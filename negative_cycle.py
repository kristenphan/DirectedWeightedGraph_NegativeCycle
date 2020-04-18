#Uses python3

import sys

# this function takes in n, the number of vertices in a directed graph, and cost, a list of weights of all edges in the graph
# the function iterate through all edges and
# returns a list of nodes with negative outgoing edges
# example:
# input:
# n = 3
# cost = [[-5], []]
#           0    1 <----- each index number represents a vertex
# output: lst = [0] because there's an outgoing edge from vertex 0 with weight of -5
def find_nodes_with_neg_edge(n, cost):
    # create a list of the start vertex of all negative edges
    lst = []
    for i in range(n):
        if len(cost[i]) > 0:
            for j in range(len(cost[i])):
                if cost[i][j] < 0:
                    lst.append(i)

    return lst

# this function performs depth-first-search from vertex s using the adjacent list representation of a directed graph (adj)
# and returns True if there's a cycle in the traversal path. otherwise, return False
# after exploring all reachable vertices from s, the function resets the visit marker (visited)
# to allow the vertices to be re-visited from another vertex that belongs to a different path
def dfs_with_reset(s, adj, visited):
    visited[s] = True
    for adj_node in adj[s]:
        if visited[adj_node]:
            visited[adj_node] = False
            visited[s] = False
            return True
        found = dfs_with_reset(adj_node, adj, visited)
        if found:
            visited[s] = False
            return True
    visited[s] = False


# this function is a wrapper function to check if there a cycle on a path rooted in s
# by calling in dfs_with_reset()
def check_for_cycle(s, adj):
    visited = [False for _ in range(len(adj))]
    return dfs_with_reset(s, adj, visited)


# this function performs depth-first-search on a path rooted in s using the adjacent list presentation of the graph (adj),
# the visited marker (visited),
# and marks all nodes visited on the traversal path
def dfs_no_reset(s, adj, visited, v):
    visited[s] = True
    v.append(s)
    for adj_node in adj[s]:
        if not visited[adj_node]:
            dfs_no_reset(adj_node, adj, visited, v)


# this function is a wrapper function to find all reachable nodes from vertex s on a directed graph represented by an adjacent list (adj)
# the function returns n, number of reachable vertices, and v, list of all reachable vertices
def find_reachable_vertices(s, adj):
    visited = [False for _ in range(len(adj))]
    v = []
    dfs_no_reset(s, adj, visited, v)
    n = visited.count(True)
    assert n == len(v)
    return n, v


# this function is part of the bellman-ford algorithm implementation
# the function performs a relaxation procedure on an edge connecting start_node and end_node with weight w by comparing the distance values (dist)
# as part of the bellman-ford algorithm implementation, it's leveraged to detect if any relaxation was possible on v-th iteration which signals a negative cycle in the graph
# the function True if relaxation occurs on v-th iteration (ie iteration count = 1)
def relax(start_node, end_node, w, dist, iteration_count):
    if dist[end_node] > dist[start_node] + w:
        dist[end_node] = dist[start_node] + w
        if iteration_count == 1:
            return True


# the function traverses through reachable vertices from s and attempts to relax the edges connecting them
# the function will also mark the vertices visited on the traversal path
# the function returns True if there's a negative cycle on the graph
def relax_all_reachable_vertices(v, adj, cost, dist, iteration_count, visited):
    for start_node in v:
        if len(adj[start_node]) > 0:
            for i in range(len(adj[start_node])):
                end_node = adj[start_node][i]
                w = cost[start_node][i]
                visited[start_node] = True
                visited[end_node] = True
                found = relax(start_node, end_node, w, dist, iteration_count)
                if found:
                    return found

# this function implements the Bellman-Ford algorithm
# to check if there's a negative cycle on a directed graph rooted in s and represented by an adjacent list (adj)
# in order to form a negative cycle, the cycle must have at least one negative edge
# so the function takes in s which represents a node with negative outgoing edge(s)
# the function applies the bellman-ford algorithm on all nodes reachable from s and detect if there's a negative cycle on the path
# if yes, return True. otherwise, return False
def bellman_ford(s, adj, cost, dist, visited):
    # count number of vertices n in path rooted in s
    n, v = find_reachable_vertices(s, adj)
    iteration_count = n
    # relax all edges on path rooted in s for n times
    while iteration_count > 0:
        found = relax_all_reachable_vertices(v, adj, cost, dist, iteration_count, visited)
        if found:
            return True
        iteration_count -= 1

    return False


# this function takes in an adjacent list representation of directed, weighted graph (adj & cost) with n vertices and m edges
# and check if there's a negative cycle on this graph
# the bellman-ford algorithm will be implemented to detect a negative cycle
# however, instead of applying it on all edges irrespective of weights,
# the algorithm will be applied only on edges on a path which contains at least one negative edge
# the rationale is that if a path does not have any negative negative, it can't have a negative cycle
# if yes, return 1. otherwise, return 0
def negative_cycle(adj, cost, n, m):
    dist = [float('inf') for _ in range(n)]
    dist[0] = 0
    visited = [False for _ in range(n)]

    lst_of_nodes_with_neg_edge = find_nodes_with_neg_edge(n, cost)
    # return 0 if there are no negative edges
    if len(lst_of_nodes_with_neg_edge) == 0:
        return 0

    # iterate through list of nodes with negative outgoing edges
    # from each node, depth-first-search through all reachable nodes and check if there's a cycle in the graph
    # if no, return 0
    # if yes, use bellman-ford() to check if the cycle is a negative cycle
    for s in lst_of_nodes_with_neg_edge:
        found = check_for_cycle(s, adj)
        # no cycle is found in the path rooted from s --> no negative cycles --> check the next node with negative outgoing edge(s)
        if found is None:
            continue
        # if the node has not been visited in previous calls to bellman-ford,
        # use bellman_ford() to detect a negative cycle on a path rooted in this node
        if not visited[s]:
            found = bellman_ford(s, adj, cost, dist, visited)
            if found:
                return 1

    return 0


# this program reads the input, builds an adjacent list representation of a directed, weighted graph (adj) with their weights stored in cost
# the program prints 1 if there's a cycle of negative weight in the graph and print 0 if there's none
if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n, m = data[0:2]
    data = data[2:]
    edges = list(zip(zip(data[0:(3 * m):3], data[1:(3 * m):3]), data[2:(3 * m):3]))
    data = data[3 * m:]
    adj = [[] for _ in range(n)]
    cost = [[] for _ in range(n)]
    for ((a, b), w) in edges:
        adj[a - 1].append(b - 1)
        cost[a - 1].append(w)

    print(negative_cycle(adj, cost, n, m))
