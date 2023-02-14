import winsound

import ctypes

import generator

import parameter
from utils import get_input

import threading
from threading import Thread, Timer
import time

from solver import backtrack, branch_and_bound, constrain_programing, dcflow, genetic_algorithm, linear_programming, \
    random


# 'test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min,parameter.N_max, parameter.M_min, parameter.M_max, parameter.K_min, parameter.K_max, parameter.Density_min, T), 'w'

class Grader(Thread):
    def __init__(self, _solver, _N, _M, _K, _linked):
        Thread.__init__(self)
        self.solver, self._N, self._M, self._K, self._linked = _solver, _N, _M, _K, _linked
        self.start_time = None
        self.end_time = None
        self.ret = None
        self.exception = None

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def interupt(self):
        self.end_time = time.time()
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def run(self):
        self.start_time = time.time()
        Timer(parameter.wait, self.interupt).start()
        try:
            self.ret = self.solver(self._N, self._M, self._K, self._linked)
        except Exception as e:
            self.exception = e
        self.end_time = time.time()

    def get_time(self):
        if self.end_time is None:
            return parameter.wait
        else:
            return self.end_time - self.start_time

    def get_return(self):
        return self.ret


generator.generate()
T = parameter.test_num
solvers = [backtrack.solve, branch_and_bound.solve, constrain_programing.solve, dcflow.solve, genetic_algorithm.solve,
           linear_programming.solve, random.solve]

failrate = {}
average_time = {}
average_penalty = {}
for solver in solvers:
    failrate[solver.__module__] = 0
    average_time[solver.__module__] = 0
    average_penalty[solver.__module__] = 0

while T:
    T -= 1
    N, M, K, linked = get_input(
        'test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min, parameter.N_max, parameter.M_min,
                                                          parameter.M_max, parameter.K_min, parameter.K_max,
                                                          parameter.Density_min, T), linked_type='edge list')
    graders = []
    for solver in solvers:
        g = Grader(solver, N, M, K, linked)
        g.start()
        graders.append((g, solver.__module__, T))

    for g, solver, testcase in graders:
        g.join()
        a = g.get_return()
        if a is None:
            failrate[solver] += 1 / parameter.test_num
        else:
            average_penalty[solver] += a[0] / parameter.test_num
        average_time[solver] += g.get_time() / parameter.test_num

for key, value in failrate.items():
    if value:
        average_penalty[key] /= value
        average_time[key] /= value

for key, value in failrate.items():
    print(value, average_time[key], average_penalty[key])

winsound.Beep(440, 2000)
