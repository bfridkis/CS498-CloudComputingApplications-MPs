#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.

import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("OrphanPages")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

pages_with_at_least_one_link = lines.flatMap(lambda x: x.split(':')[1].split(' ')).filter(lambda x: x != '').sortBy(lambda x: x).distinct()
orphaned_links = lines.map(lambda x: x.split(':')[0]).subtract(pages_with_at_least_one_link).sortBy(lambda x: x).collect()

output = open(sys.argv[2], "w")
with output as f:
    for link in orphaned_links:
        f.write(f"{link}\n")

sc.stop()

# https://www.google.com/search?q=all+values+from+one+rdd+not+in+another+rdd+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=all+values+from+one+rdd+not+in+another+rdd+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigAdIBCDU0NzBqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

