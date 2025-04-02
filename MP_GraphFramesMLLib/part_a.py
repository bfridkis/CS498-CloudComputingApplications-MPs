from pyspark import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import collect_list
from graphframes import *

sc = SparkContext()
spark = SparkSession.builder.appName('ConnectedComponents').getOrCreate()


def get_connected_components(graphframe):
    # TODO:
    # get_connected_components is given a graphframe that represents the given graph
    # It returns a list of lists of ids.
    # For example, [[a_1, a_2, ...], [b_1, b_2, ...], ...]
    # then a_1, a_2, ..., a_n lie in the same component,
    # b_1, b2, ..., b_m lie in the same component, etc
    
    #Get connected components dataframe using graphframes "connectedComponents" methond.
    connected_components = graphframe.connectedComponents()
    
    #Establish list for return data
    list_of_connected_components = []
    
    #Load list_of_connected_components with results
    for row in connected_components.groupby('component').agg(collect_list('id').alias('node_list')).select('node_list').collect():
        list_of_connected_components.append(row.asDict()['node_list'])
    
    return list_of_connected_components
    #return [[]]


if __name__ == "__main__":
    vertex_list = []
    edge_list = []
    #with open('/MP_GraphFramesMLLib/dataset/graph.data') as f:  # DO NOT MODIFY
    with open('dataset/graph.data') as f:  # DO NOT MODIFY
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

    result = get_connected_components(g)
    for line in result:
        print(' '.join(line))
        
# https://www.google.com/search?q=how+to+build+a+graphframe+pyspark&rlz=1C1CHBF_enUS1071US1071&oq=how+to+build+a+graphframe+pyspark&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORigATIHCAEQIRigATIHCAIQIRigATIHCAMQIRiPAtIBCTE1Mzk0ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8
# https://graphframes.github.io/graphframes/docs/_site/index.html
# https://www.google.com/search?q=how+to+output+all+values+for+grouped+data+pyspark+dataframe&sca_esv=62d75a41637246f2&rlz=1C1CHBF_enUS1071US1071&ei=w17tZ4OqHfeO0PEP6uT2uQ8&oq=how+to+output+all+values+for+grouped+data+pyspark+dat&gs_lp=Egxnd3Mtd2l6LXNlcnAiNWhvdyB0byBvdXRwdXQgYWxsIHZhbHVlcyBmb3IgZ3JvdXBlZCBkYXRhIHB5c3BhcmsgZGF0KgIIADIFECEYoAEyBRAhGKABMgUQIRigAUjVO1AAWK0ycAB4AZABAJgBmQKgAY1FqgEHMC4xNi4yNrgBA8gBAPgBAZgCKqACsUbCAgUQABiABMICBhAAGBYYHsICCBAAGBYYChgewgILEAAYgAQYhgMYigXCAggQABiABBiiBMICBRAAGO8FwgIIEAAYogQYiQXCAgUQIRirAsICBRAhGJ8FmAMAkgcHMC4xMi4zMKAHhqkCsgcHMC4xMi4zMLgHsUY&sclient=gws-wiz-serp
