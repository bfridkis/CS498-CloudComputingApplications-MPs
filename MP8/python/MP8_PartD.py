from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc

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
#  4. MapReduce : List the top three words that have appeared in the
#  greatest number of years. 
#  Sorting order of the final answer should should be descending by word count,
#  then descending by word.

# Register the DataFrame as a SQL temporary view
df.createOrReplaceTempView("books")

spark.sql("Select word, COUNT(*) FROM books GROUP BY word ORDER BY COUNT(*) desc, word desc LIMIT 3").show()

# Spark SQL

# +-------------+--------+
# |         word|count(1)|
# +-------------+--------+
# |    ATTRIBUTE|      11|
# |approximation|       4|
# |    agast_ADV|       4|
# +-------------+--------+
# only showing top 3 rows

