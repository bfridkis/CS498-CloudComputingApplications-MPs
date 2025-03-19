import sys
import boto3
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from pyspark.sql.functions import col, when
from pyspark.sql.types import IntegerType

## @params: ["JOB_NAME"]
args = getResolvedOptions(sys.argv, ["JOB_NAME"])
# Get Spark context
sc = SparkContext()
# From spark context get glue context and spark session
glueContext = GlueContext(sc)
# set custom logging on
logger = glueContext.get_logger()
# Create and init job
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Begin TODOs - add your code starting from here. Comments
# are provided for each statement that you may need to add.

# 1. Create a Glue client to access the Data Catalog API
client = boto3.client('glue')

# 2. Create a dynamic frame from AWS Glue catalog table. In the following lines
# use the create_dynamic_frame.from_catalog() API of the GlueContext class. Use
# the Glue catalog database and table name (output of job 1) as arguments.
dynamic_frame = glueContext.create_dynamic_frame.from_catalog("mp9-flights", "transformed-flights-data-1")

# 3. Get Spark dataframe from the Glue dynamic frame created above
#spark_df = dynamic_frame.toDF(options={"inferSchema": "true"})
spark_df = dynamic_frame.toDF()

# 4. Create a new time_zone_difference column and add it to the Spark data frame.
# See the MP description on how to calculate the value of the time zone
# difference between the arrival and departure airports. You may need to check the
# data type when doing the time zone difference calculations to get the correct values.
# time_zone_difference = (f1.scheduled_arrival / 100)*60 + (f1.scheduled_arrival % 100) - ((f1.scheduled_departure / 100)*60 + (f1.scheduled_departure % 100) + f1.scheduled_time)%(24*60)
# spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", (((spark_df.scheduled_arrival / 100).cast('int')*60 + \
                                                                              # (spark_df.scheduled_arrival % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                              # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
# spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & (col("scheduled_departure") - col("scheduled_arrival") >= 1200), 
                                                                                   # ((((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   # ((spark_df.scheduled_arrival+2400) % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                             # .otherwise(((spark_df.scheduled_arrival+2400 / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_arrival+2400 % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                        # (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
spark_df_w_time_zone_difference = spark_df.withColumn("time_zone_difference", when((col("scheduled_arrival") < col("scheduled_departure")) & (col("scheduled_time") >= 60), 
                                                                                   ((((spark_df.scheduled_arrival+2400) / 100).cast('int')*60 + \
                                                                                   ((spark_df.scheduled_arrival) % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                   (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))
                                                                             .otherwise(((spark_df.scheduled_arrival / 100).cast('int')*60 + \
                                                                                        (spark_df.scheduled_arrival % 100) - ((spark_df.scheduled_departure / 100).cast('int')*60 + \
                                                                                        (spark_df.scheduled_departure % 100) + spark_df.scheduled_time))%(24*60)))

# 5. Convert Spark data frame back to Glue dynamic frame
# Note - you can do step 4 using AWS Glue dynamic frame APIs also if you want
# to avoid steps 3 and 5. However, it maybe easier to do the transformations
# in step 4 using Spark data frame.
dynamic_frame_w_tzd = DynamicFrame.fromDF(spark_df_w_time_zone_difference, glueContext, 'dynamic_frame_w_tzd')
#DynamicFrame.fromDF(spark_df_w_time_zone_difference, glueContext, 'dynamic_frame_w_tzd')

# 6. Get the existing Glue catalog table schema. You can use the glue client
# created in step 1 and use its get_table() API to get the table schema which
# will be a python dictionary. You can see the response of get_table() here:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/get_table.html
try:
    response = client.get_table(
        DatabaseName = "mp9-flights",
        Name = "transformed-flights-data-1"
    )
    original_table = response['Table']
    new_table = original_table.copy()
except Exception as e:
    #print(f"Error retrieving table metadata: {e}")
    logger.info(f"Error retrieving table metadata: {e}")
    exit()

# 7. Delete the following fields in the table schema dictionary as
# the update_table API gives ParamValidationError when these fields are present:
# 'UpdateTime', 'IsRegisteredWithLakeFormation', 'CreatedBy', 'DatabaseName',
# 'CreateTime', 'CatalogId'. If there is an error related to 'VersionId', that
# field also needs to be deleted.
for key in ['UpdateTime', 'IsRegisteredWithLakeFormation', 'CreatedBy', 'DatabaseName', 'CreateTime', 'CatalogId', 'VersionId', 'IsMultiDialectView']:
    del new_table[key]
new_table["Name"] = "transformed-flights-data-2"

# 8. Define the new column 'time_zone_difference' to be added to the table schema

# 9. Append the new column info to the table dictionary (obtained in step 6) columns list
#print(new_table)
logger.info(f"new_table: {new_table}") 
new_table["StorageDescriptor"]["Columns"].append({'Name': 'time_zone_difference', 'Type': 'bigint'})
new_table["StorageDescriptor"]["Location"] = "s3://fridkis-mp9-flights-dataset/Transformed-Output/Glue-Job-2/"

# 10. Update the table with the new schema. Use the update_table() API of glue client:
# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glue/client/update_table.html
try:
    # response = client.update_table(
        # DatabaseName="mp9-flights",
        # TableInput=new_table
    # )
    # #print(f"Table updated successfully for {new_table}")
    # logger.info(f"Table updated successfully for {new_table}")
    response = client.create_table(
        DatabaseName="mp9-flights",
        TableInput=new_table,
    )
    #print(f"Table updated successfully for {new_table}")
    logger.info(f"Table created successfully for {new_table}") 
except Exception as e:
    #print(f"Error updating table: {e}")
    logger.info(f"Error creating table: {e}") 
    
# 11. Get the output S3 bucket in which the transformed table data will be
# stored. Use the getSink() API of the GlueContext class.
#https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html
data_sink = glueContext.getSink(
    path="s3://fridkis-mp9-flights-dataset/Transformed-Output/Glue-Job-2/",
    connection_type="s3",
    enableUpdateCatalog=True,
)
    
# 12. Set the catalog database and table using the setCatalogInfo() API on
# the object obtained in step 11.
#data_sink.setCatalogInfo(catalogDatabase="mp9-flights", catalogTableName="transformed-flights-data-1")
data_sink.setCatalogInfo(catalogDatabase="mp9-flights", catalogTableName="transformed-flights-data-2")

# 13. Set the format to 'json' using setFormat() API
data_sink.setFormat("json")

# 14. Write data into S3 bucket using writeFrame()
data_sink.writeFrame(dynamic_frame_w_tzd)

# End TODOs

# Commit job
job.commit()

# References
# https://www.google.com/search?q=change+schema+amazon+glue+python+example&rlz=1C1CHBF_enUS1071US1071&oq=change+schema+amazon+glue+python+example&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigAdIBCDY2NjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_catalog
# https://stackoverflow.com/questions/53137425/create-dynamic-frame-from-catalog-returning-zero-results
# https://stackoverflow.com/questions/33681487/how-do-i-add-a-new-column-to-a-spark-dataframe-using-pyspark
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.withColumn.html
# https://www.google.com/search?q=withColumn+conditional+logic+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=withColumn+conditional+logic+pyspark&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yDQgCEAAYhgMYgAQYigUyDQgDEAAYhgMYgAQYigUyDQgEEAAYhgMYgAQYigUyCggFEAAYgAQYogTSAQg3NDU0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://stackoverflow.com/questions/59014650/convert-spark-dataframe-to-aws-glue-dynamic-frame
# https://www.google.com/search?q=how+to+use+boto+get_table+and+update_table+glue+python&rlz=1C1CHBF_enUS1071US1071&oq=how+to+use+boto+get_table+and+update_table+glue+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRigATIHCAIQIRigATIHCAMQIRigAdIBCTE5MTQ4ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://stackoverflow.com/questions/48914324/how-do-i-write-messages-to-the-output-log-on-aws-glue
# https://stackoverflow.com/questions/72091152/aws-user-not-authorized-to-perform-passrole (glue job 3)