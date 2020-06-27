import numpy as np



def cost(cost_mat, route):
    return cost_mat[np.roll(route, 1), route].sum()

def cost_change(cost_mat, n1, n2, n3, n4):
    return cost_mat[n1][n3] + cost_mat[n2][n4] - cost_mat[n1][n2] - cost_mat[n3][n4]


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


if __name__ == '__main__':
    nodes = 50
    init_route = list(range(nodes))
    # print(init_route)
    cost_np_matrix = np.random.randint(100, size=(nodes, nodes))
    # cost_np_matrix = np.array([[0, 47554, 29399, 9110, 27827, 41484, 7554, 53099, 68759, 9098],
    #             [51143, 0, 55354, 56707, 55400, 52145, 55151, 42666, 58725, 56695],
    #             [32900, 60064, 0, 25841, 16330, 29096, 24479, 24273, 42132, 22916],
    #             [8760, 56259, 25368, 0, 22786, 36443, 2889, 41193, 49202, 4057],
    #             [27880, 61778, 16406, 22855, 0, 14622, 21493, 19621, 27381, 19931],
    #             [41374, 52306, 34783, 36349, 14795, 0, 34988, 16832, 18545, 33425],
    #             [7339, 54839, 23562, 2787, 20503, 34160, 0, 38440, 46919, 1774],
    #             [56453, 42418, 25165, 41420, 19899, 13542, 40783, 0, 21635, 38495],
    #             [73903, 65096, 42119, 49199, 27644, 18670, 47837, 15226, 0, 46274],
    #             [9084, 56584, 22906, 4060, 19847, 33504, 2698, 37785, 46263, 0]])

    cost_mat = cost_np_matrix.T
    np.fill_diagonal(cost_mat, 0)
    cost_mat = list(cost_mat)
    best_route = two_opt(init_route, cost_mat)
    # best_route_cost = cost(cost_np_matrix, best_route)
    print(f'Best Route: {best_route}')
    # print(f'Best Route Cost: {best_route_cost}')
