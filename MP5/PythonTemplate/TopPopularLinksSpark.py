#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 
#lines = sc.textFile('dataset/links/', 1)

# Works locally but would not pass auto-grader because it is very memory intensive (doesn't spread memory load), causes "java.io.IOException - Failed to connect to ip..." error) - See additional resources on TitleCoutSpark.py.
#results = sorted(lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).countByValue().items(), key = lambda kv: (kv[1], kv[0]))[-10:]

# From https://www.google.com/search?q=use+reduce+to+count+occurrences+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=use+reduce+to+count+occurrences+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRiPAtIBCDY3NTFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8 
def count_occurrences(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = result.get(key, 0) + value
    return result

# # This didn't work either. Ran successfully locally, but was very slow and also would not pass the autograder with was appeared to also be a memory issue. Same "java.io.IOException" error. 
# results = sorted(lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).map(lambda x: {x: 1}).reduce(count_occurrences).items(), key = lambda kv: (kv[1], kv[0]))[-10:]

#Use map and reduceByKey funtions instead of countByValue or reduce - Could also consider using RDD.sortBy() or RDD.sortByKey() instead of sorting returned dataset locally
results = sorted(lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).map(lambda x: (x, 1)).reduceByKey(lambda x, y: x + y).collect(), key = lambda kv: (kv[1], kv[0]))[-10:]

output = open(sys.argv[2], "w")
with output as f:
    for(link,count) in sorted(results):
        f.write(f"{link}\t{count}\n")

#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()

# Reference
# https://stackoverflow.com/questions/72709396/java-io-ioexception-in-local-spark-mode
