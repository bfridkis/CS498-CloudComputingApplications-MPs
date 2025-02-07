#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopPopularLinks")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1) 
#lines = sc.textFile('dataset/links/', 1)

# results = lines.flatMap(lambda x: x.split(':')[1][1:].split(' '))
# results_counted = results.countByValue()
#results = lines.map(lambda x: x.split(':')[1][1:].split(' ')).flatMap(lambda x: x).countByValue()
#results = lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).countByValue().items()
results = sorted(lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).countByValue().items(), key = lambda kv: (kv[1], kv[0]))[-5:]

output = open(sys.argv[2], "w")
with output as f:
    for(link,count) in sorted(results):
        f.write(f"{link}\t{count}\n")

#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

sc.stop()

