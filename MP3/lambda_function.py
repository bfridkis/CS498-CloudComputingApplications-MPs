import json
from collections import deque
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MP3-DistanceGraph')

def lambda_handler(event, context):
    
    print(f"event: {event}")

    results = process_graph(event)

    scan = table.scan(
        ProjectionExpression='#k,#sk',
        ExpressionAttributeNames={
        '#k': 'source',
        '#sk': 'destination'
        }
    )

    #print(scan['Items'])

    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(Key=each)

    #print("Starting table update loop...")
    #for each in results:
    #    print(f"Should be adding: {each}")
    #    source = each[0]
    #    distance = each[2]
    #    destination = each[1]
    #    table.put_item(Item={'source': source, 'distance': distance, 'destination': destination})
    #    table.put_item(Item=each)

    # Create list of put requests for batch write operations
    put_requests = [{'PutRequest': {'Item': result}} for result in results]

    # Split the results list into batches of 25 items (DynamoDB batch write limit)
    for batch in [put_requests[i:i + 25] for i in range(0, len(put_requests), 25)]:
        request_items = {'MP3-DistanceGraph': batch}
        
        # Perform batch write operation
        response = dynamodb.batch_write_item(RequestItems=request_items)
        
        # Check if any unprocessed items
        while 'UnprocessedItems' in response:
            # Retry with the unprocessed items if any
            unprocessed_items = response['UnprocessedItems']
            if not unprocessed_items:
                break  # No more unprocessed items, exit the loop
            updates = {table_name: unprocessed_items}
            response = dynamodb.batch_write_item(RequestItems=updates)
    
    ## Check if all items were successfully added
    if not response.get('UnprocessedItems'):
        print("All items added successfully")
    else:
        print("Some items were not added successfully")
            
    # Alternate method for writing in batches, but not sure how to get/monitor unprocessed requests this way...i.e. not sure how/where to get 'response'
    #for batch in [results[i:i + 25] for i in range(0, len(results), 25)]:
        #updates = batch
        #with table.batch_writer(overwrite_by_pkeys=['source', 'distance']) as writer:
            #for each in updates:
                #source = each['source']
                #distance = each['distance']
                #destination = each['destination']
                #batch.put_item(Item={'source': source, 'distance': distance, 'destination': destination})
                #response = writer.put_item(Item=each)
                #while 'UnprocessedItems' in response:
                # Retry with the unprocessed items if any
                #    unprocessed_items = response['UnprocessedItems']
                #    if not unprocessed_items:
                #        break  # No more unprocessed items, exit the loop
                #    response = writer.put_item(Item=unprocessed_items)

    return {
        'statusCode': 200,
        #'body': json.dumps('Hello from Lambda!')
        'body': json.dumps(results)
    }

def process_graph(graph='{"graph": "Chicago->Urbana,Urbana->Springfield,Chicago->Lafayette"}'):
    try:
        graph_data_str = json.loads(graph)["graph"]
    except:
        graph_data_str = graph["graph"]
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
    
    shortest_paths = []
    for source in graph_dict:
        distances = bfs_shortest_paths(graph_dict, source)
        for destination, distance in distances.items():
            #shortest_paths.append((source, destination, distances[destination]))
            shortest_paths.append({"source": source, "destination": destination, "distance": distance})
    
    return shortest_paths

# REFERENCES:   
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+python&rlz=1C1GCCA_enUS1080US1080&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDY0MjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

# The Function Below Is Taken directly from GoogleAI search (with slight modification)
# From Google AI overview: search prompt - "breadth first search to find shortest path unweighted edges python"
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+python&rlz=1C1GCCA_enUS1080US1080&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDY0MjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
def bfs_shortest_paths(graph, start):
    """
    Finds the shortest paths from a start node to all other nodes in an unweighted graph.

    Args:
        graph (dict): The graph represented as an adjacency list.
        start (int): The starting node.

    Returns:
        dict: A dictionary where keys are nodes and values are their distances from the start node.
    """

    distances = {node: -1 for node in graph}
    distances[start] = 0
    queue = deque([start])

    while queue:
        current_node = queue.popleft()

        for neighbor in graph[current_node]:
            if distances[neighbor] == -1:
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)

    return distances

# References
# https://gist.github.com/Swalloow/9966d576a9aafff482eef6b59c222baa
# From Google AI overview: search prompt - "breadth first search to find shortest path unweighted edges python"
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+python&rlz=1C1GCCA_enUS1080US1080&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDY0MjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8
# https://aws.plainenglish.io/luit-project-12-using-boto3-python-to-add-items-in-a-dynamodb-table-c12acda7701d