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
# 5. Joining : The following program construct a new dataframe out of 'df' with a much smaller size.
####

df2 = df.select("word", "year").distinct().orderBy("year", "word").limit(100)
df2.createOrReplaceTempView('gbooks2')

#result = spark.sql("SELECT COUNT(*) FROM gbooks2 AS gb1 JOIN gbooks2 AS gb2 ON gb1.word != gb2.word AND gb1.year == gb2.year")
result = spark.sql("SELECT COUNT(*) FROM gbooks2 AS gb1 JOIN gbooks2 AS gb2 ON gb1.year == gb2.year")

result.first()['count(1)']

# Now we are going to perform a JOIN operation on 'df2'. Do a self-join on 'df2' in lines with the same #'count1' values and see how many lines this JOIN could produce. Answer this question via Spark SQL API

# Spark SQL API

# output: 310

