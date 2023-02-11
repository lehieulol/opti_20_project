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


def solve(vB, vA, vC, vD):
    model = cp_model.CpModel()

    # Building model by Licht using edge list
    N, M, K, linked = vB, vA, vC, vD
    edges = [model.NewIntVar(0, 1, '') for _ in linked]
    papers = [model.Add()]
    judge = [model.Add()]

    penalty = model.NewIntVar(0, N, '')
    model.AddMaxEquality(penalty, judge)
    

    # Building model
    vX = [[model.NewIntVar(0, 1, "") for p in range(vB)] for s in range(vA)]
    # C1
    for p in range(vB):
        model.Add(sum(vX[s][p] for s in range(vA)) >= vC)
    # C2
    for p in range(vB):
        for s in range(vA):
            if (s + 1) in vD[p]: continue  # Skip if Scientist s can work on Paper p
            model.Add(vX[s][p] == 0)
    # Objective
    vY = model.NewIntVar(0, vB, "")
    model.AddMaxEquality(vY, [sum(vX[s][p] for p in range(vB)) for s in range(vA)])
    model.Minimize(vY)

    # Print solution
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = parameter.wait - 2
    status = solver.Solve(model)
    if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        matrix = [['#' if (solver.Value(vX[s][p])) else '.' for s in range(vA)] for p in range(vB)]
        return solver.Value(vY), matrix
    else:
        return 'No solution found', []
