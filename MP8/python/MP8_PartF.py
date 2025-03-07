from pyspark.sql.functions import col, lag
from pyspark import SparkContext
from pyspark.sql.types import StructType
from pyspark.sql.types import StructField
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import *

sc = SparkContext()
spark = SparkSession.builder.getOrCreate()

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

###
# 2. Frequency Increase : analyze the frequency increase of words starting from the year 1500 to the year 2000
###
# Spark SQL - DataFrame API

df_years_filtered = df.filter(df['year'] >= 1500).filter(df['year'] <= 2000)
#df_years_filtered.createOrReplaceTempView("books_years_1500to2000")

w = Window.partitionBy("word").orderBy("year")
df_word_increase_intermediate = df_years_filtered.withColumn("previous_frequency", lag("frequency", 1, 0).over(w))
#df_years_filtered.withColumn("previous_value", lag("year", 1, 0).over(w)).show()

#df_word_increase_intermediate.createOrReplaceTempView("books_with_frequency_increase")
#spark.sql("Select * FROM books_with_frequency_increase ORDER BY previous_value DESC LIMIT 20").show()
#spark.sql("Select word, SUM(previous_frequency) as total_increase FROM books_with_frequency_increase PARTITION BY word ORDER BY total_increase DESC LIMIT 20").show()

#df_word_increase.show()