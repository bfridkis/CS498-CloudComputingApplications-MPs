from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()

####
# 1. Setup : Write a function to load it in an RDD & DataFrame

#Load RDD from file/disk, split on tabs (rdd_split is a list of lists), and convert strings to ints (columns 2-4)
rdd = sc.textFile("gbooks", 1)
#rdd = sc.textFile("/MP8/python/gbooks", 1)
rdd_split = rdd.map(lambda line: line.split("\t")).map(lambda line: [line[0],int(line[1]),int(line[2]),int(line[3])])
####

# RDD API
# Columns:
# 0: word (string), 1: year (int), 2: frequency (int), 3: books (int)

#Declare dataframe schema
schema = StructType([
    StructField("word", StringType(), True),
    StructField("year", IntegerType(), True),
    StructField("frequency", IntegerType(), True),
    StructField("books", IntegerType(), True)
    ])

#Load dataframe from rdd
df = spark.createDataFrame(rdd_split, schema)

#show dataframe
df.printSchema()


# Spark SQL - DataFrame API

# REFERENCES
# https://www.google.com/search?q=how+to+load+rdd+into+sql+dataframe+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=how+to+load+rdd+into+sql+dataframe+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRifBTIHCAQQIRifBdIBCDk4OTRqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrame.html
# https://www.google.com/search?q=how+to+load+tab+seperated+rdd+into+sql+dataframe+pyspark&sca_esv=333b08b6cdc38758&rlz=1C1CHBF_enUS1071US1071&ei=6yPKZ-ixOrjCp84PsqyD0A0&ved=0ahUKEwio0_zUwvaLAxU44ckDHTLWANoQ4dUDCBA&uact=5&oq=how+to+load+tab+seperated+rdd+into+sql+dataframe+pyspark&gs_lp=Egxnd3Mtd2l6LXNlcnAiOGhvdyB0byBsb2FkIHRhYiBzZXBlcmF0ZWQgcmRkIGludG8gc3FsIGRhdGFmcmFtZSBweXNwYXJrMggQABiABBiiBDIIEAAYgAQYogQyCBAAGIAEGKIEMggQABiABBiiBDIIEAAYogQYiQVIriNQ2QlYmiFwAXgBkAEBmAH1AaABxhGqAQYwLjEzLjG4AQPIAQD4AQGYAgqgApELwgIKEAAYsAMY1gQYR8ICBRAAGO8FmAMAiAYBkAYIkgcDMS45oAe4Tw&sclient=gws-wiz-serp
# https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.SparkSession.createDataFrame.html
# https://spark.apache.org/docs/3.5.2/sql-getting-started.html

