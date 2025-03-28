-- Paragraph 1

%flink.ssql(type=update)

-- create a table to glue data catalog table with columns for stock data, 
-- sets a watermark to trigger late arrival events, and configures it to read 
-- from a Kinesis stream, in JSON format with an ISO-8601 timestamp format.
CREATE TABLE stock_table(
    `date` STRING,
    ticker VARCHAR(6),
    open_price FLOAT,
    high FLOAT,
    low FLOAT,
    close_price FLOAT,
    adjclose FLOAT,
    volume BIGINT,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time as event_time
) WITH ( --connect to your kinesis data stream
    'connector' = 'kinesis', 
    --'stream.arn' = 'arn:aws:kinesis:us-east-1:024848464133:stream/mp10-kinesis-data-stream',
    'stream' = 'mp10-kinesis-data-stream',
    'aws.region' = 'us-east-1',
    'scan.stream.initpos' = 'LATEST',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601'
);

DROP TABLE IF EXISTS part_a;
DROP TABLE IF EXISTS part_b;
DROP TABLE IF EXISTS part_c;
CREATE TABLE part_a(event_time TIMESTAMP(3), cmgr FLOAT, `date` STRING, close_price FLOAT) 
WITH ('connector' = 'filesystem','path' = 's3://mp10-flink-application-code/part_a','format' = 'json','json.timestamp-format.standard' = 'ISO-8601');
CREATE TABLE part_b(ticker VARCHAR(6), `date` STRING, close_price FLOAT, avg_close_price FLOAT, ema_close_price DOUBLE)
WITH ('connector' = 'filesystem','path' = 's3://mp10-flink-application-code/part_b','format' = 'json','json.timestamp-format.standard' = 'ISO-8601');
CREATE TABLE part_c(ticker VARCHAR(6), event_time TIMESTAMP(3), initialPriceDate STRING, dropDate STRING, dropPercentage DOUBLE, initialPrice FLOAT, lastPrice FLOAT)
WITH ('connector' = 'filesystem','path' = 's3://mp10-flink-application-code/part_c','format' = 'json','json.timestamp-format.standard' = 'ISO-8601');

----------------------

-- Paragraph 2

%flink.pyflink

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf


# Define the custom function
@udf(result_type=DataTypes.FLOAT(), input_types=[DataTypes.FLOAT(), DataTypes.STRING()])
def to_cmgr(close_price: float, date: str) -> float:
    # Get day, month, year
    date_tokens = date.split("/")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    
    # Return 0 if record is from Jan 2021, or day of month is > 3rd
    if (month == 1 and year == 2021) or day > 3:
        return 0
    
    else:
        cmgr = (((close_price/92.30)**(1/((month-1)+(12*(year%2021)))))-1)*100
        # Return the compound monthly growth rate
        return cmgr

# Register the custom function with a name
st_env.create_temporary_function("to_cmgr", to_cmgr)


----------------------

-- Paragraph 3

%flink.ssql(runAsOne=True)

INSERT INTO part_a
    SELECT event_time, to_cmgr(close_price, `date`) AS cmgr, `date`, close_price FROM
    (
        SELECT event_time, to_cmgr(close_price, `date`) AS cmgr, `date`, close_price 
        FROM stock_table
    ) AS t
    WHERE t.cmgr <> 0
;

INSERT INTO part_b
    SELECT * FROM (    
        SELECT ticker, `date`, close_price, avg_close_price, 
        exp(((SUM(ln(close_price)) OVER (
            PARTITION BY ticker
            ORDER BY `event_time`
            ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
            ))/10)) AS ema_close_price
        FROM (
            SELECT ticker, `date`, close_price, avg_close_price, event_time
            FROM (
                SELECT
                    event_time,
                    `date`,
                    ticker,
                    close_price,
                    AVG(close_price) OVER (
                        PARTITION BY ticker
                        ORDER BY event_time
                        ROWS BETWEEN 9 PRECEDING AND CURRENT ROW
                    ) AS avg_close_price
                FROM stock_table
            ) t
        -- WHERE close_price < avg_close_price
        ) 
    ) WHERE close_price < ema_close_price
;

INSERT INTO part_c
    SELECT *
    FROM stock_table
        MATCH_RECOGNIZE (
          PARTITION BY ticker
          ORDER BY event_time
          MEASURES
            A.event_time AS event_time,
            A.`date` AS InitialPriceDate,
            C.`date` AS dropDate,
            -100*(C.close_price - A.close_price)/A.close_price AS dropPercentage,
            A.close_price AS InitialPrice,
            C.close_price AS lastPrice
          ONE ROW PER MATCH
          AFTER MATCH SKIP PAST LAST ROW
          PATTERN (A B{0,2} C)
          -- PATTERN (A+ B)
          -- PATTERN (A B)
          DEFINE
            -- A AS A.close_price = 0
            -- A AS A.close_price > B.close_price AND A.close_price > C.close_price,
            -- A AS A.close_price > C.close_price,
            B AS -100*(B.close_price - A.close_price)/A.close_price < 8.0,
            -- C AS -100*(C.close_price - A.close_price)/A.close_price >= 8.0
            C AS C.close_price < A.close_price AND -100*(C.close_price - A.close_price)/A.close_price >= 8.0
        ) AS T
;
