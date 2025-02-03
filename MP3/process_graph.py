import json
import sys
sys.path.append("C:\\Users\\fridkbj\\OneDrive - Phillips 66\\Documents\\UIUC Masters\\CS498-CloudComputingApplications\\CS498-CloudComputingApplications-MPs\\MP3\\")
from googleAIbreadthfirst import bfs_shortest_paths

def process_graph(graph='{"graph": "Chicago->Urbana,Urbana->Springfield,Chicago->Lafayette"}'):
graph_data_str = json.loads(graph)["graph"]
graph_dict = {}

edges = graph_data_str.split(",")

for edge in edges:
    source, destination = edge.split("->")
    if source in graph_dict and destination not in graph_dict[source]:
        graph_dict[source].append(destination)
    else:
        graph_dict[source] = [destination]
    if destination not in graph_dict:
        graph_dict[destination] = []

# REFERENCES:   
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+python&rlz=1C1GCCA_enUS1080US1080&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDY0MjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8