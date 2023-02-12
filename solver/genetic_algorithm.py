import random

from bitarray import bitarray, util
import time

import parameter
from utils import ELtoM


def solve(N, M, K, linked):

    start_time = time.time()
    population_size = len(linked)
    next_population_size = int(population_size*.1)
    print('population_size:', population_size, '| next_population_size:', next_population_size)
    bit_len = len(linked)
    # randomized population
    current_population = []

    def eval(bit_array):
        return real_penalty(bit_array)

    def real_penalty(bit_array):
        count_n = [0 for _ in range(N)]
        count_m = [0 for _ in range(M)]
        for i in range(len(bit_array)):
            if bit_array[i]:
                count_n[linked[i][0] - 1] += 1
                count_m[linked[i][1] - 1] += 1
        # illegal solution
        if min(count_n) < K:
            return float('inf')
        return max(count_m)

    def crossover(_par_1, _par_2):
        assert len(_par_1) == bit_len
        assert len(_par_2) == bit_len
        a, b = random.randint(0, bit_len), random.randint(0, bit_len)
        if a > b:
            a, b = b, a
        _child_1 = _par_1[0:a]+_par_2[a:b]+_par_1[b:bit_len]
        _child_2 = _par_2[0:a]+_par_1[a:b]+_par_2[b:bit_len]
        return _child_1, _child_2

    # point mutation
    def mutation(bit_array_1):
        mutation_rate = .8
        while random.random() < mutation_rate:
            try:
                a = random.randrange(0, bit_len)
                bit_array_1[a] ^= 1
            except:
                print('a:',a,'bit_len:',len(bit_array_1))
                print(bit_array_1)
        return bit_array_1

    # select 2 parent to make offspring
    def selection():
        # select 70% (30%-1%) , 0% (80%-31%), 30% (81%-100%)
        cut = [0, .3, .8, 1.]
        distribution = [.7, .0, .3]
        # decide which cut this parent will be in
        chosen_cut = [random.choices(range(len(distribution)), weights=distribution)[0], random.choices(range(len(distribution)), weights=distribution)[0]]
        # decide what sample is chosen
        chosen_sample = [current_population[random.randrange(int(cut[i] * population_size), int(cut[i + 1] * population_size))][0] for i in chosen_cut]
        return chosen_sample

    for _ in range(population_size):
        temp = util.urandom(bit_len)
        if random.random() < 0.7:
            temp.setall(1)
        current_population.append((temp, eval(temp)))

    best = None

    while True:
        # get the best individual
        current_population.sort(key=lambda x: x[1])
        best = current_population[0]
        if time.time() - start_time > parameter.wait - 1:
            break
        next_population = []
        while len(next_population) < next_population_size:
            par_1, par_2 = selection()
            child_1, child_2 = crossover(par_1, par_2)
            child_1 = mutation(child_1)
            child_2 = mutation(child_2)
            next_population.append((child_1, eval(child_1)))
            next_population.append((child_2, eval(child_2)))
        current_population = current_population[0: (population_size-next_population_size)]
        current_population += next_population

    if best is None or real_penalty(best[0]) == float('inf'):
        return None
    else:
        return real_penalty(best[0]), ELtoM(N, M, edge_list=linked, picked=best[0])
