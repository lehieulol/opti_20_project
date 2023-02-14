# ===============================[ Problem ]=============================
# There are vA scientists who need to work on vB papers.
# Each paper requires (at least) vC scientists.
# An array vD of length vB will specify which scientist can work on which paper.
# Goal: Minimize the number of papers each scientist works on.
# ===============================[ Model 1 ]=============================
# Vars:
#  vX[s, p] == 1 means whether Scientist s works on Paper p
#  Domain(vX[s, p]) === (0, 1)
# Constrains:
#  sum(vX[s, p] foreach Scientist s) >= vC foreach Paper p
#  vX[ vD[p, i], p ] == 0 foreach Paper p and i in vD[p]
#   // A scientist can NOT work on this paper
# Objective:
#  Minimize max( sum(vX[s, p] foreach Paper p) foreach Scientist s )
# =======================================================================

# Import
from ortools.sat.python import cp_model

import parameter


def solve(N, M, K, linked):
    model = cp_model.CpModel()

    # Building model by Licht using edge list
    edges = { edge: model.NewIntVar(0, 1, '') for edge in linked }
    papers = []
    judges = []

    # Populate sum alias
    for p in range(N):
        papers.append(sum( var for edge, var in edges.items() if edge[0]-1 == p ))
    for j in range(M):
        judges.append(sum( var for edge, var in edges.items() if edge[1]-1 == j ))

    # Penalty is the maximum numbers of papers each judge works on
    penalty = model.NewIntVar(0, N, '')
    model.AddMaxEquality(penalty, judges)

    # Constrain: A paper requires at least K judges
    for p in range(N):
        model.Add(papers[p] >= K)

    # Objective: Minimize number of papers worked on by any judges
    model.Minimize(penalty)

    # Print solution
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = parameter.wait - 1
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        matrix = []
        for p in range(N):
            # Build line
            line = [ solver.Value(edges[p, j]) if (p, j) in edges else 0 for j in range(M) ]
            matrix.append(['#' if column else '.' for column in line])
        return solver.Value(penalty), matrix
    else:
        return None
