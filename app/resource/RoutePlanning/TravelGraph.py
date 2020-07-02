from pprint import pprint
from sys import maxsize
import numpy as np

# implementation of traveling Salesman Problem

class TSPMatrix():

    def __init__(self, **kwargs):
        self.matrix = kwargs.get('matrix', [])
        self.location_list = kwargs.get('location_list', [])
        self.mapping_list = kwargs.get('mapping_list', [])
        

    def from_gmaps_matrix(self, gmaps_matrix_dict:dict, **kwargs):

        """
        mode = select one from ('distance', 'duration', 'duration_in_traffic')
        mapping_list = using index mapping the mapping_list 
        """
        self.location_list = kwargs.get('location_list', [])
        self.mapping_list = kwargs.get('mapping_list', gmaps_matrix_dict['origin_addresses'])
        mode = kwargs.get('mode', 'distance')

        if gmaps_matrix_dict['status'] == 'OK':
            origin_addresses = gmaps_matrix_dict['origin_addresses']
            destination_addresses = gmaps_matrix_dict['destination_addresses']
            rows = gmaps_matrix_dict['rows']
            for row in rows:
                el_list = []
                for element in row['elements']:
                    # if element['status'] == 'OK':
                    el_list.append(element[mode]['value'])
                self.matrix.append(el_list)
            # pprint(self.matrix)
        return self

class TSP(TSPMatrix):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def normal_ans(self, start=0, **kwargs):

        graph = kwargs.get('graph', self.matrix)

        # store all vertex apart from source vertex
        V = len(graph)
        # V = 4
        s = start
        vertex = []
        for i in range(V):
            if i != s:
                vertex.append(i)
        # store minimum weight Hamiltonian Cycle
        min_path = maxsize
        Visted_dict = {}

        # next_permutation implementation
        def next_permutation(L):
            # It will change the list L.
            n = len(L)
            i = n - 2
            while i >= 0 and L[i] >= L[i + 1]:
                i -= 1
            if i == -1:
                return False
            j = i + 1
            while j < n and L[j] > L[i]:
                j += 1
            j -= 1
            L[i], L[j] = L[j], L[i]
            left = i + 1
            right = n - 1
            while left < right:
                L[left], L[right] = L[right], L[left]
                left += 1
                right -= 1
            return True

        while True:
            # store current Path weight(cost)
            current_pathweight = 0
            # compute current path weight
            k = s
            for i in range(len(vertex)):
                current_pathweight += graph[k][vertex[i]]
                k = vertex[i]
            # current_pathweight += graph[k][s]
            Visted_dict[current_pathweight] = list(vertex) #用list把它給實例化並存在dict裡，
            # update minimum
            min_path = min(min_path, current_pathweight)
            if not next_permutation(vertex):
                break
        Visted_dict[min_path].insert(0, s)
        # Visted_dict[min_path].append(s)
        order_location_list = [self.location_list[i] for i in Visted_dict[min_path]] if self.location_list else Visted_dict[min_path]
        order_mapping_list = [self.mapping_list[i] for i in Visted_dict[min_path]] if self.mapping_list else Visted_dict[min_path]
        return (min_path,order_location_list, order_mapping_list)

    def backtracking_ans(self, start=0, **kwargs):

        graph = kwargs.get('graph', self.matrix)

        def tsp(graph, v, currPos, n, count, cost): 
            # If last node is reached and it has  
            # a link to the starting node i.e  
            # the source then keep the minimum  
            # value out of the total cost of  
            # traversal and "ans" 
            # Finally return to check for  
            # more possible values 
            if (count == n and graph[currPos][0]): 
                answer.append(cost + graph[currPos][0])
                return 
                # return cost + graph[currPos][0]
        
            # BACKTRACKING STEP 
            # Loop to traverse the adjacency list 
            # of currPos node and increasing the count 
            # by 1 and cost by graph[currPos][i] value 
            for i in range(n): 
                if (v[i] == False and graph[currPos][i]): 
                    # Mark as visited 
                    v[i] = True
                    tsp(graph, v, i, n, count + 1, cost + graph[currPos][i]) 
                    # Mark ith node as unvisited 
                    v[i] = False

        n = len(graph)
        v = [False for i in range(n)] 
        v[start] = True
        answer = []
        tsp(graph, v, 0, n, 1, 0)

        return min(answer)

    def two_opt_ans(self, start=0, **kwargs):

        graph = kwargs.get('graph', self.matrix)

        def cost_change(cost_mat, n1, n2, n3, n4):
            return cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]

        def cost(cost_mat, route):
            return cost_mat[np.roll(route, 1), route].sum()

        def two_opt(route, cost_mat):
            best = route
            improved = True
            while improved:
                improved = False
                for i in range(1, len(route) - 2):
                    for j in range(i + 1, len(route)):
                        if j - i == 1:
                            continue
                        if cost_change(cost_mat, best[i - 1], best[i], best[j - 1], best[j]) < 0:
                            best[i:j] = best[j - 1:i - 1:-1]
                            improved = True
                route = best
            return best

        nodes = len(graph)
        cost_np_matrix = np.array(graph)
        init_route = list(range(nodes))
        cost_mat = cost_np_matrix.T
        np.fill_diagonal(cost_mat, 0)
        cost_mat = list(cost_mat)
        best_route = two_opt(init_route, cost_mat)
        best_route_cost = cost(cost_np_matrix, best_route)
        print(f'Best Route: {best_route}')
        print(f'Best Route Cost: {best_route_cost}')
        order_location_list = [self.location_list[i] for i in best_route] if self.location_list else best_route
        order_mapping_list = [self.mapping_list[i] for i in best_route] if self.mapping_list else best_route
        return (best_route_cost, order_location_list, order_mapping_list)