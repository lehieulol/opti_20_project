import parameter
import random
from math import ceil

TRIES = 1000 # TODO: replace with time

def solve(N, M, K, linked):
    edges = { edge: False for edge in linked }

    papers = lambda _edges, p: sum(var for edge, var in _edges.items() if edge[0]-1 == p) # number of judges for a paper
    judges = lambda _edges, j: sum(var for edge, var in _edges.items() if edge[1]-1 == j) # number of papers for a judge
    penalty = lambda _edges: max(papers(_edges, j) for j in range(M)) # objective
    valid = lambda _edges: all([ papers(_edges, p) >= K for p in range(N) ]) # check if constrain is satified

    minPossible = ceil(N * K / M) # Best possible penalty

    # Use adjacent matrix
    allowed = [[] for _ in range(N)]
    for edge in linked:
        allowed[edge[0]-1].append(edge[1]-1)

    # Greedy algo for best state
    paperChoices = [] # Choices for random guess
    for p in range(N):
        if len(allowed[p]) < K:
            return "No solution" # INFEASABLE
        elif len(allowed[p]) == K:
            for j in allowed[p]:
                edges[p+1, j+1] = True
            continue

        # Assign this paper to judges currently have lowest paper count
        allowed[p].sort(key = lambda j: judges(edges, j))
        for j in allowed[p][:K]:
            edges[p+1, j+1] = True
        paperChoices.append(p)

    # Set best
    bestEdges = edges.copy()
    bestPenalty = penalty(edges)

    for _ in range(TRIES):
        if bestPenalty <= minPossible:
            break

        # Pick random paper and random allowed judge
        # then toggle judge working that paper
        p = random.choice(paperChoices)
        j = random.choice(allowed[p])
        edges[p+1, j+1] = not edges[p+1, j+1]

        # SKip if not valid
        if not valid(edges):
            continue

        # Update if better
        newPenalty = penalty(edges)
        if newPenalty < bestPenalty:
            newPenalty = bestPenalty
            bestEdges = edges.copy()

    # Output
    matrix = []
    for p in range(N):
        line = [ bestEdges[p, j] if (p, j) in bestEdges else False for j in range(M) ]
        matrix.append(['#' if column else '.' for column in line])
    return bestPenalty, matrix
