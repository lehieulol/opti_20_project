import generator

import parameter
from utils import get_input
import Backtrack

# 'test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min,parameter.N_max, parameter.M_min, parameter.M_max, parameter.K_min, parameter.K_max, parameter.Density_min, T), 'w'

T = parameter.test_num
while T:
    T -= 1
    N, M, K, linked = get_input(
        'test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min, parameter.N_max, parameter.M_min,
                                                          parameter.M_max, parameter.K_min, parameter.K_max,
                                                          parameter.Density_min, T))
    print(Backtrack.solve(N, M, K, linked))