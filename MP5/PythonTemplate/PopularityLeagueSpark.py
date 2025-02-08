#!/usr/bin/env python
# Use LF instead of CRLF for end-of-line in files for Windows compatibility.
#Execution Command: spark-submit PopularityLeagueSpark.py dataset/links/ dataset/league.txt
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("PopularityLeague")
conf.set("spark.driver.bindAddress", "127.0.0.1")
sc = SparkContext(conf=conf)

lines = sc.textFile('dataset/links/')
lines = sc.textFile(sys.argv[1], 1) 


leagueIds = sc.textFile('dataset/league2.txt')
leagueIds = sc.textFile(sys.argv[2], 1)
leagueIdslist = leagueIds.collect()

# Works locally but would not pass auto-grader because it is very memory intensive (doesn't spread memory load), causes "java.io.IOException - Failed to connect to ip..." error) - See additional resources on TitleCoutSpark.py.
#results = lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).filter(lambda x: x in leagueIdslist).countByValue()

# From https://www.google.com/search?q=use+reduce+to+count+occurrences+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=use+reduce+to+count+occurrences+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRiPAtIBCDY3NTFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8 
def count_occurrences(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        result[key] = result.get(key, 0) + value
    return result
    
# Use map and reduce funtions instead of countByValue
results = lines.flatMap(lambda x: x.split(':')[1][1:].split(' ')).filter(lambda x: x in leagueIdslist).map(lambda x: {x: 1}).reduce(count_occurrences)

# Reference
# https://www.google.com/search?q=group+by+values+dictionary+python&rlz=1C1CHBF_enUS1071US1071&oq=group+by+values+dictionary+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgWGB4yBwgCEAAY7wUyCggDEAAYgAQYogQyBwgEEAAY7wXSAQg4MjgwajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
def group_by_values(input_dict):
    """Groups keys of a dictionary by their values.
    
    Args:
        input_dict: The dictionary to group by values.
...
    Returns:
        A new dictionary where keys are the unique values from the input
        dictionary and values are lists of keys that had that value in the
        input dictionary.
    """
    grouped_dict = {}
    for key, value in input_dict.items():
        grouped_dict.setdefault(value, []).append(key)
    return grouped_dict
    
grouped_results = sorted(group_by_values(results).items())
cur_rank = 0
rankings = []  
for count in sorted(grouped_results):
    if len(count[1]) == 1:
        rankings.append((count[1][0], cur_rank))
        cur_rank = cur_rank + 1
    else:
        for link in sorted(count[1]):
            rankings.append((link, cur_rank))
        cur_rank = cur_rank + len(count[1])

#TODO
#write results to output file. Foramt for each line: (key + \t + value +"\n")

output = open(sys.argv[3], "w")
with output as f:
    for link, rank in sorted(rankings):
        f.write(f"{link}\t{rank}\n")

sc.stop()

# References
# https://www.google.com/search?q=intersect+but+keep+duplicates+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=intersect+but+keep+duplicates+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRigATIHCAQQIRiPAtIBCTEwMDE2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8