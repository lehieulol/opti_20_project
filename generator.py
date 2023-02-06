import random

import parameter
from random import randint, shuffle

T = parameter.test_num
while T:
    T -= 1
    N = randint(parameter.N_min, parameter.N_max)
    M = randint(parameter.M_min, parameter.M_max)
    K = randint(parameter.K_min, parameter.K_max)

    linked = []
    for i in range(N+1):
        linked.append([])

    connections = []

    for _ in range(1, N+1):
        for __ in range(1, M+1):
            connections.append((_, __))

    shuffle(connections)

    countdown = N
    num_link = 0
    for _ in connections:
        if countdown == 0 and num_link/(N*M) >= parameter.Density_min:
            break
        linked[_[0]].append(_[1])
        num_link += 1
        if len(linked[_[0]]) == K:
            countdown -= 1
    f = open('test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min,parameter.N_max, parameter.M_min, parameter.M_max, parameter.K_min, parameter.K_max, parameter.Density_min, T), 'w')
    f.write('{} {} {}\n'.format(N, M, K))

    for _ in linked:
        if _:
            f.write('{} '.format(len(_)))
            for __ in _:
                f.write('{} '.format(__))
            f.write('\n')
    f.close()