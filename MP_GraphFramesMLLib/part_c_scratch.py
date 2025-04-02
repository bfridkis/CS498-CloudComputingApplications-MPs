from pyspark import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import collect_list
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('ShortestPath').getOrCreate()


def get_shortest_distances(graphframe, dst_id):
    # TODO
    # Find shortest distances in the given graphframe to the vertex which has id `dst_id`
    # The result is a dictionary where key is a vertex id and the corresponding value is
    # the distance of this node to vertex `dst_id`.
    
    #Get connected components dataframe using graphframes "connectedComponents" methond.
    shortest_paths = graphframe.shortestPaths(landmarks=[dst_id])
    
    #Establish list for return data
    dict_of_shortest_paths = {}
    
    #Load list_of_connected_components with results
    for row in shortest_paths.collect():
        if not row.asDict()['distances'] == {}:
            dict_of_shortest_paths[row.asDict()['id']] = row.asDict()['distances']['1']
        else:
            dict_of_shortest_paths[row.asDict()['id']] = -1
    
    return dict_of_shortest_paths
    #return {}

vertex_list = []
edge_list = []
with open('/MP_GraphFramesMLLib/dataset/graph.data') as f:  # DO NOT MODIFY
    for line in f:
        nodes = line.split()
        src = nodes[0]  # TODO: Parse src from line
        dst_list = nodes[1:]  # TODO: Parse dst_list from line
        vertex_list.append((src,))
        edge_list += [(src, dst) for dst in dst_list]

#vertices = spark.createDataFrame(vertex_list,["id", "name"])  # TODO: Create vertices dataframe
vertices = spark.createDataFrame(vertex_list,["id"])  # TODO: Create vertices dataframe
edges = spark.createDataFrame(edge_list,["src", "dst"])  # TODO: Create edges dataframe

g = GraphFrame(vertices, edges)
sc.setCheckpointDir("/tmp/connected-components")

# We want the shortest distance from every vertex to vertex 1
for k, v in get_shortest_distances(g, '1').items():
    print(k, v)