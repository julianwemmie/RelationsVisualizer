from node import Node

# TODO: implement dijkstras algorthim into main app

def dijkstra(nodes, start, stop):
    visited = []
    touched = []
    shortest_prev_node = {}
    node_weights = {}
    current = start

    node_weights[start.name] = 0
    shortest_prev_node[start.name] = start.name
    touched.append(start.name)

    while current != stop:        
        for touching in current.edges:
            # ignore already visited nodes
            if touching.name in visited:
                continue

            relation = tuple(sorted([current.name, touching.name]))
            relation_weight = Node.edge_weights[relation]
            current_weight = node_weights[current.name]
            cumulative_weight = current_weight + relation_weight

            # add weight if doesn't exist
            if touching.name not in node_weights.keys():
                node_weights[touching.name] = cumulative_weight
                shortest_prev_node[touching.name] = current.name

            # if exists, update with smallest weight and path
            elif node_weights[touching.name] > cumulative_weight:
                node_weights[touching.name] = cumulative_weight
                shortest_prev_node[touching.name] = current.name

            touched.append(touching.name)
        
        # move current node from touched to visited
        visited.append(current.name)
        touched.remove(current.name)

        # get the weights of only touched nodes
        toVisit = dict(filter(lambda item: item[0] in touched, node_weights.items()))

        # returns key of the smallest weight
        current = min(toVisit, key = toVisit.get)

        # get Node object from name (which is a string)
        current = nodes.get(current)

    final_weight = node_weights[stop.name]

    return (shortest_prev_node, final_weight)
