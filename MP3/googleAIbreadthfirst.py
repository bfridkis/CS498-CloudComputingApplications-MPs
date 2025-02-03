from collections import deque

def bfs_shortest_path(graph, start, goal):
    """Finds the shortest path between two nodes in an unweighted graph using BFS."""

    queue = deque([(start, [start])])  # Queue of (node, path) tuples
    visited = set()

    while queue:
        node, path = queue.popleft()

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                queue.append((neighbor, path + [neighbor]))

    return None  # No path found

# Example usage:
# graph = {
    # 'A': ['B', 'C'],
    # 'B': ['A', 'D', 'E'],
    # 'C': ['A', 'F'],
    # 'D': ['B'],
    # 'E': ['B', 'F'],
    # 'F': ['C', 'E']
# }

# start_node = 'A'
# end_node = 'F'

# shortest_path = bfs_shortest_path(graph, start_node, end_node)

# if shortest_path:
    # print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
# else:
    # print(f"No path found from {start_node} to {end_node}")
    
# From Google AI overview: search prompt - "breadth first search to find shortest path unweighted edges python"
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+python&rlz=1C1GCCA_enUS1080US1080&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+python&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDY0MjhqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

from collections import deque

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

# Example usage:
# graph = {
    # 0: [1, 2],
    # 1: [0, 3],
    # 2: [0, 4],
    # 3: [1, 4],
    # 4: [2, 3]
# }

# start_node = 0
# shortest_paths = bfs_shortest_paths(graph, start_node)

# print(shortest_paths)

# From Google AI overview: search prompt - "breadth first search to find shortest path unweighted edges for all nodes python"
# https://www.google.com/search?q=breadth+first+search+to+find+shortest+path+unweighted+edges+for+all+nodes+python&sca_esv=e43f164304cbaefd&rlz=1C1GCCA_enUS1080US1080&ei=HxyhZ9_0MPjhp84Ptfyv2Ac&ved=0ahUKEwifgJG7oaiLAxX48MkDHTX-C3sQ4dUDCBA&uact=5&oq=breadth+first+search+to+find+shortest+path+unweighted+edges+for+all+nodes+python&gs_lp=Egxnd3Mtd2l6LXNlcnAiUGJyZWFkdGggZmlyc3Qgc2VhcmNoIHRvIGZpbmQgc2hvcnRlc3QgcGF0aCB1bndlaWdodGVkIGVkZ2VzIGZvciBhbGwgbm9kZXMgcHl0aG9uSO8xUK4OWNIwcAJ4AZABAJgBvQGgAcELqgEDOC42uAEDyAEA-AEBmAIEoAL1AcICChAAGLADGNYEGEfCAgQQIRgKmAMAiAYBkAYIkgcDMi4yoAe1Kg&sclient=gws-wiz-serp