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

# Spark SQL - DataFrame API

####
# 2. Counting : How many lines does the file contains? Answer this question via both RDD api & #Spark SQL
####

# Register the DataFrame as a SQL temporary view
df.createOrReplaceTempView("books")

# Run count query
spark.sql("Select COUNT(*) FROM books").show()

# Spark SQL 

# sqlContext.sql(query).show() or df.show()
# +--------+
# |count(1)|
# +--------+
# |   50013|
# +--------+

# REFERENCES
# https://spark.apache.org/docs/3.5.2/sql-getting-started.html
