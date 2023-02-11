from .backtrack import solve as BTSolver
from .branch_and_bound import solve as BBSolver
from .constrain_programing import solve as CPSolver
from .dcflow import solve as DCFSolver
from .genetic_algorithm import solve as GASolver
from .linear_programming import solve as LPSolver
from .random import solve as RSolver

allSolvers = [
    BTSolver,
    BBSolver,
    CPSolver,
    DCFSolver,
    GASolver,
    LPSolver,
    RSolver,
]
