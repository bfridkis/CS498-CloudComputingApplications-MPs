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

----------------------

%flink.ssql(type=update)
-- SHOW TABLES;
DESCRIBE stock_table;
-- SELECT * FROM stock_table;
-- SELECT date FROM stock_table WHERE date = '1/4/2021';
-- SELECT COUNT(*) FROM stock_table;

----------------------

-- This is just an example from here: https://docs.aws.amazon.com/managed-flink/latest/java/how-zeppelin-sql-examples.html#how-zeppelin-examples-creating-tables
%flink.pyflink
from pyflink.table.table import Table

def as_view(table, name):
  if (name in st_env.list_temporary_views()):
    st_env.drop_temporary_view(name)
  st_env.create_temporary_view(name, table)
  return table

Table.as_view = as_view

----------------------

-- Example from assignment prompt
%flink.pyflink

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, DataTypes
from pyflink.table.udf import udf


# Define the custom function
@udf(result_type=DataTypes.FLOAT(), input_types=[DataTypes.FLOAT(), DataTypes.FLOAT()])
def to_average(low: float, high: float) -> float:
    # Calculate the average of low and high
    avg = (low + high) / 2
    # Return the result
    return avg

# Register the custom function with a name
st_env.create_temporary_function("to_average", to_average)

----------------------

-- Example from assignment prompt
%flink.ssql(type=update)

SELECT low, high, event_time, to_average(low, high) AS avg_price
FROM stock_table

----------------------

%flink.ssql(type=update)

DROP TEMPORARY FUNCTION IF EXISTS to_cmgr;

----------------------

-- Exercise A
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

-- Exercise A
%flink.ssql(type=update)

SELECT event_time, cmgr, `date`, close_price FROM
(
    SELECT event_time, to_cmgr(close_price, `date`) AS cmgr, `date`, close_price 
    FROM stock_table
)
WHERE cmgr <> 0

----------------------

-- Exercise B
%flink.ssql
/* stock prices of when the current price is lower than the moving average which would be a good indicator for a bear market*/
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

-- Exercise C
%flink.ssql
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
        -- A AS A.close_price = 0  -- This wasn't behaving as expected, but not sure why...
        -- A AS A.close_price > B.close_price AND A.close_price > C.close_price,  -- This wasn't working either, no matches... I think because it can't look ahead (e.g. can't compare A to B or C in A's definition but can do vis versa...)
        -- A AS A.close_price > C.close_price, -- This wasn't working either, no matches... I think because it can't look ahead (e.g. can't compare A to B or C in A's definition but can do vis versa...)
        B AS -100*(B.close_price - A.close_price)/A.close_price < 8.0,
        -- C AS -100*(C.close_price - A.close_price)/A.close_price >= 8.0
        C AS C.close_price < A.close_price AND -100*(C.close_price - A.close_price)/A.close_price >= 8.0
) AS T

-- REFERENCES
-- https://nightlies.apache.org/flink/flink-docs-release-1.20/docs/connectors/table/kinesis/
-- https://docs.aws.amazon.com/managed-flink/latest/java/how-zeppelin-sql-examples.html#how-zeppelin-examples-creating-tables
-- https://nightlies.apache.org/flink/flink-docs-release-2.0/docs/dev/table/sql/queries/match_recognize/