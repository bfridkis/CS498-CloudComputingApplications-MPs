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

result = get_connected_components(g)
for line in result:
	print(' '.join(line))