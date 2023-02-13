from collections import deque

'''
Idea:
We can check if each judge take at most A then every paper have K judge (1) by this idea:
    Make a directed graph:
    sink -- K --> N paper -- 1 --> M judge -- A --> source
    If max flow of this equal N*K then (1) is true
    
if with A_0, (1) is true; with A >= A_0 (1) is true
if with A_0, (1) is false; with A <= A_0 (1) is false
with this we have a binary patern of (1) 000...00[1]1...111

We want to find minimun A so that (1) is true
Using divide and conquer we can achive that
With A_min found, using dinic algorigthm we can found exactly what edge from N papers to M judges chosen
'''


def solve(N, M, K, linked):
    """

    :param N:
    :param M:
    :param K:
    :param linked: "edge list"
    :return:
    """

    # Max Flow: Dinic Algorigthm
    class Edge:
        def __init__(self, v, flow, C, rev):
            self.v = v
            self.flow = flow
            self.C = C
            self.rev = rev

    class Graph:
        def __init__(self, V):
            self.adj = [[] for i in range(V)]
            self.V = V
            self.level = [0 for i in range(V)]

        def addEdge(self, u, v, C):

            # Forward edge : 0 flow and C capacity
            a = Edge(v, 0, C, len(self.adj[v]))

            # Back edge : 0 flow and 0 capacity
            b = Edge(u, 0, 0, len(self.adj[u]))
            self.adj[u].append(a)
            self.adj[v].append(b)

        # Finds if more flow can be sent from s to t
        # Also assigns levels to nodes
        def BFS(self, s, t):
            for i in range(self.V):
                self.level[i] = -1

            # Level of source vertex
            self.level[s] = 0

            # Create a queue, enqueue source vertex
            # and mark source vertex as visited here
            # level[] array works as visited array also
            q = deque()
            q.append(s)
            while q:
                u = q.popleft()
                for i in range(len(self.adj[u])):
                    e = self.adj[u][i]
                    if self.level[e.v] < 0 and e.flow < e.C:
                        # Level of current vertex is
                        # level of parent + 1
                        self.level[e.v] = self.level[u] + 1
                        q.append(e.v)

            # If we can not reach to the sink we
            # return False else True
            return False if self.level[t] < 0 else True

        def sendFlow(self, u, flow, t):
            # Sink reached
            if u == t:
                return flow

            # Traverse all adjacent edges one -by -one
            remaining_flow = flow
            for e in self.adj[u]:
                # Pick next edge from adjacency list of u
                if self.level[e.v] == self.level[u] + 1 and e.flow < e.C:
                    # find minimum flow from u to t
                    curr_flow = min(remaining_flow, e.C - e.flow)
                    temp_flow = self.sendFlow(e.v, curr_flow, t)

                    # flow is greater than zero
                    if temp_flow > 0:
                        # add flow to current edge
                        e.flow += temp_flow

                        # subtract flow from reverse edge
                        # of current edge
                        self.adj[e.v][e.rev].flow -= temp_flow

                    remaining_flow -= temp_flow
            return flow - remaining_flow

        def DinicMaxflow(self, s, inflow, t):
            # Corner case
            if s == t:
                return -1

            # Initialize result
            total = 0

            # Augument the flow while there is path
            # from source to sink
            while self.BFS(s, t):
                # store how many edges are visited
                # from V { 0 to V }
                flow = self.sendFlow(s, inflow, t)
                if not flow:
                    break
                total += flow

            # return maximum flow
            return total
    # Max Flow: end

    # Divide and Conquer the result
    upper_bound = N
    lower_bound = 1
    while upper_bound != lower_bound:
        middle_point = (upper_bound + lower_bound) // 2
        # graph: source - N paper - M judge - sink
        g = Graph(N+M+2)
        # from source to N paper capacity K the amount required for each paper
        for i in range(1, N+1):
            g.addEdge(0, i, K)
        # from N paper to M judge
        for u, v in linked:
            g.addEdge(u, v+N, 1)
        # from M judge to sink
        for i in range(1, M + 1):
            g.addEdge(N+i, N+M+1, middle_point)

        # check if we can flow through all N papers with K capacity

        if g.DinicMaxflow(0, N*K, N+M+1) == N*K:
            upper_bound = middle_point
        else:
            lower_bound = middle_point + 1

    # we get lower_bound = upper_bound = middle_point as the minimum paper for judge
    # graph: source - N paper - M judge - sink
    g = Graph(N + M + 2)
    # from source to N paper capacity K
    for i in range(1, N + 1):
        g.addEdge(0, i, K)
    # from N paper to M judge
    for u, v in linked:
        g.addEdge(u, v+N, 1)
    # from M judge to sink
    for i in range(1, M + 1):
        g.addEdge(N + i, N + M + 1, lower_bound)
    g.DinicMaxflow(0, N*M, N+M+1)
    matrix = []
    for i in range(1, N+1):
        matrix.append(['.' for _ in range(M)])
        for e in g.adj[i]:
            if e.flow == 1:
                matrix[-1][e.v-N-1] = '#'
    return lower_bound, matrix

