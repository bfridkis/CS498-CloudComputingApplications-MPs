#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("TopTitleStatistics")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1], 1)

Mean = int(lines.map(lambda x: int(x.split('\t')[1])).mean() // 1)
Sum = lines.map(lambda x: int(x.split('\t')[1])).sum()
Min = lines.map(lambda x: int(x.split('\t')[1])).min()
Max = lines.map(lambda x: int(x.split('\t')[1])).max()
Variance = int(lines.map(lambda x: int(x.split('\t')[1])).variance())

outputFile = open(sys.argv[2], "w")
'''
TODO write your output here
write results to output file. Format
outputFile.write('Mean\t%s\n' % ans1)
outputFile.write('Sum\t%s\n' % ans2)
outputFile.write('Min\t%s\n' % ans3)
outputFile.write('Max\t%s\n' % ans4)
outputFile.write('Var\t%s\n' % ans5)
'''

outputFile.write(f"Mean\t{Mean}\n")
outputFile.write(f"Sum\t{Sum}\n")
outputFile.write(f"Min\t{Min}\n")
outputFile.write(f"Max\t{Max}\n")
outputFile.write(f"Var\t{Variance}\n")

sc.stop()

