#!/usr/bin/env python

# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
'''Exectuion Command: spark-submit TitleCountSpark.py stopwords.txt delimiters.txt dataset/titles/ dataset/output'''

import sys
from pyspark import SparkConf, SparkContext

stop_words_path = sys.argv[1]
delimiters_path = sys.argv[2]
#stopWords = []
#delimiters = []

with open(stop_words_path) as f:
	stop_words = [word.rstrip() for word in f]
stop_words.append('')

with open(delimiters_path) as f:
    delimiters = list([line for line in f][0])

conf = SparkConf().setMaster("local").setAppName("TitleCount")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[3], 1)

def split_line(delimiters):
    def _split_line(line):
        for delimiter in delimiters:
            line = line.replace(delimiter, ' ')
        return line
    return _split_line
    
def filter_word(stop_words):
    def _filter_word(word):
        return word not in stop_words
    return _filter_word
    
output = sorted(lines.map(split_line(delimiters)).flatMap(lambda x: x.split(' ')).map(lambda x: x.lower()).filter(filter_word(stop_words)).countByValue().items(), key = lambda kv: (kv[1], kv[0]))[-10:]
    
outputFile = open(sys.argv[4],"w")
with outputFile as f:
    for(w,c) in sorted(output):
        f.write(f"{w}\t{c}\n")

#write results to output file. Foramt for each line: (line +"\n")

sc.stop()


# References
# https://medium.com/analytics-vidhya/how-does-pyspark-work-step-by-step-with-pictures-c011402ccd57
# https://www.google.com/search?q=pyspark+counting+example+no+dataframe&sca_esv=d4768e3d9c71eb29&rlz=1C1CHBF_enUS1071US1071&ei=m02lZ56OENLCp84P5K_syQg&ved=0ahUKEwjex7mbobCLAxVS4ckDHeQXO4kQ4dUDCBI&uact=5&oq=pyspark+counting+example+no+dataframe&gs_lp=Egxnd3Mtd2l6LXNlcnAiJXB5c3BhcmsgY291bnRpbmcgZXhhbXBsZSBubyBkYXRhZnJhbWUyBRAhGKABMgUQIRigATIFECEYoAEyBRAhGKABMgUQIRifBUiMMVCUB1iKL3ACeACQAQCYAYABoAGJDaoBBDIuMTO4AQPIAQD4AQGYAhCgAusMwgIKEAAYsAMY1gQYR8ICBhAAGBYYHsICCxAAGIAEGIYDGIoFwgIFEAAY7wXCAggQABiiBBiJBcICBRAhGKsCmAMAiAYBkAYIkgcEMy4xM6AHsVU&sclient=gws-wiz-serp
# https://stackoverflow.com/questions/28999332/how-to-access-sparkcontext-in-pyspark-script
# https://stackoverflow.com/questions/33019420/spark-rdd-mapping-with-extra-arguments