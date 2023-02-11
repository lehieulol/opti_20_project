from ortools.linear_solver import pywraplp
from math import ceil
import parameter

def solve(N, M, K, linked):
    solver = pywraplp.Solver('minimize_maximum_papers',
                             pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)

    # Building model by Licht using edge list
    edges = { edge: solver.IntVar(0, 1, '') for edge in linked }
    papers = []
    judges = []

    # Populate sum alias
    for p in range(N):
        papers.append(solver.Sum( var for edge, var in edges.items() if edge[0]-1 == p ))
    for j in range(M):
        judges.append(solver.Sum( var for edge, var in edges.items() if edge[1]-1 == j ))

    # Penalty is the maximum numbers of papers each judge works on
    penalty = solver.IntVar(0, N, '')
    for j in range(M):
        solver.Add(judges[j] <= penalty)

    # Constrain: A paper requires at least K judges
    for p in range(N):
        solver.Add(papers[p] >= K)

    # Objective: Minimize number of papers worked on by any judges
    solver.Minimize(penalty)

    # Print solution
    # solver.parameters.max_time_in_seconds = parameter.wait - 2
    status = solver.Solve()
    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        matrix = []
        for p in range(N):
            # Build line
            line = [ edges[p, j].solution_value() if (p, j) in edges else 0 for j in range(M) ]
            matrix.append(['#' if column else '.' for column in line])
        return ceil(penalty.solution_value()), matrix
    else:
        return 'No solution found', []
