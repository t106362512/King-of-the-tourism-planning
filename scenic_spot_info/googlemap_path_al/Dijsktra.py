from collections import defaultdict

class Graph():
    def __init__(self):
        """
        self.edges is a dict of all possible next nodes
        e.g. {'X': ['A', 'B', 'C', 'E'], ...}
        self.weights has all the weights between two nodes,
        with the two nodes as a tuple as the key
        e.g. {('X', 'A'): 7, ('X', 'B'): 2, ...}
        """
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        # Note: assumes edges are bi-directional
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight
        return self

class GraphAlgorithm(Graph):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Enjoy the Algorithm!!!")

    def from_gmaps_matrix(self, gmaps_matrix_dict:dict):
        if gmaps_matrix_dict['status'] == 'OK':
            origin_addresses = gmaps_matrix_dict['origin_addresses']
            destination_addresses = gmaps_matrix_dict['destination_addresses']
            rows = gmaps_matrix_dict['rows']
            ddict = defaultdict(list)
            for row_ind, row in enumerate(rows):
                for el_ind, element in enumerate(row['elements']):
                    # if row_ind != el_ind:
                    ddict[(origin_addresses[row_ind], destination_addresses[el_ind])] = element['distance']['value']
            self._add_dict_bulk(ddict)
        return self

    def _add_dict_bulk(self, graph_dict:dict):
        for from_to_nodes, weight in graph_dict.items():
            self.add_edge(from_to_nodes[0], from_to_nodes[1], weight)
        return self
    
    def dijsktra(self, initial, end, **kwargs):
        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        graph = kwargs.get('graph', self)
        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()
        
        while current_node != end:
            visited.add(current_node)
            destinations = graph.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = graph.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)
            
            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return "Route Not Possible"
            # next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        
        # Work back through destinations in shortest path
        path = []
        while current_node is not None:
            path.append(current_node)
            next_node = shortest_paths[current_node][0]
            current_node = next_node
        # Reverse path
        path = path[::-1]
        return path

# class TSP:
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.order = []
#         print("Enjoy the Algorithm!!!")

#     def add_edge(self, from_node, to_node, weight, *args, **kwargs):
#         super().add_edge(from_node, to_node, weight, *args, **kwargs)
#         self.order.append(from_node) if from_node not in self.order else None

#     def add_dict_bulk(self, graph_dict:dict):
#         for from_to_nodes, weight in graph_dict.items():
#             self.add_edge(from_to_nodes[0], from_to_nodes[1], weight)
#         return self

#     def _to_matrix(self, **kwargs):
#         order = kwargs.get('order', self.order)
#         matrix = []
#         for index, ord in enumerate(order):
#             for ord in enumerate(order):
#             self.weights[(ord, )]
#         pass

# if __name__ == "__main__":
#     graph = Graph()
#     edges = [
#         ('X', 'A', 7),
#         ('X', 'B', 2),
#         ('X', 'C', 3),
#         ('X', 'E', 4),
#         ('A', 'B', 3),
#         ('A', 'D', 4),
#         ('B', 'D', 4),
#         ('B', 'H', 5),
#         ('C', 'L', 2),
#         ('D', 'F', 1),
#         ('F', 'H', 3),
#         ('G', 'H', 2),
#         ('G', 'Y', 2),
#         ('I', 'J', 6),
#         ('I', 'K', 4),
#         ('I', 'L', 4),
#         ('J', 'L', 1),
#         ('K', 'Y', 5),
#     ]

#     for edge in edges:
#         graph.add_edge(*edge)
#     r = Graph.dijsktra(graph, 'X', 'Y')
#     print(r)
