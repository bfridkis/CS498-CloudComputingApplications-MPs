#!/usr/bin/env python

# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
from pyspark import SparkConf, SparkContext

stopWordsPath = sys.argv[1]
delimitersPath = sys.argv[2]
#stopWords = []
#delimiters = []

with open(stopWordsPath) as f:
	stopWords = [word.rstrip() for word in f]

with open(delimitersPath) as f:
    delimiters = [char for char in f]

conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[3], 1)

#TODO

outputFile = open(sys.argv[4],"w")

#TODO
#write results to output file. Foramt for each line: (line +"\n")

sc.stop()


# References
# https://medium.com/analytics-vidhya/how-does-pyspark-work-step-by-step-with-pictures-c011402ccd57
# https://www.google.com/search?q=pyspark+counting+example+no+dataframe&sca_esv=d4768e3d9c71eb29&rlz=1C1CHBF_enUS1071US1071&ei=m02lZ56OENLCp84P5K_syQg&ved=0ahUKEwjex7mbobCLAxVS4ckDHeQXO4kQ4dUDCBI&uact=5&oq=pyspark+counting+example+no+dataframe&gs_lp=Egxnd3Mtd2l6LXNlcnAiJXB5c3BhcmsgY291bnRpbmcgZXhhbXBsZSBubyBkYXRhZnJhbWUyBRAhGKABMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRifBUiMMVCUB1iKL3ACeACQAQCYAYABoAGJDaoBBDIuMTO4AQPIAQD4AQGYAhCgAusMwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIFEAAY7wXCAggQABiiBBiJBcICBRAhGKsCmAMAiAYBkAYIkgcEMy4xM6AHsVU&sclient=gws-wiz-serp