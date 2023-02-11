import ctypes

import generator

import parameter
from utils import get_input

import threading
from threading import Thread, Timer
import time

import Backtrack
import Branch_and_Bound
import DCFlow
import Constrain_Programing


# 'test/N_{}_{}_M_{}_{}_K_{}_{}_Dense_{}_{}'.format(parameter.N_min,parameter.N_max, parameter.M_min, parameter.M_max, parameter.K_min, parameter.K_max, parameter.Density_min, T), 'w'

class Grader(Thread):
    def __init__(self, _solver, _N, _M, _K, _linked):
        Thread.__init__(self)
        self.solver, self._N, self._M, self._K, self._linked = _solver, _N, _M, _K, _linked
        self.start_time = None
        self.end_time = None
        self.ret = None

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def interupt(self):
        print('interupt called')
        self.end_time = time.time()
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    def run(self):
        self.start_time = time.time()
        Timer(parameter.wait, self.interupt).start()
        self.ret = self.solver(self._N, self._M, self._K, self._linked)
        self.end_time = time.time()

    def get_time(self):
        if self.end_time is None:
            return parameter.wait
        else:
            return self.end_time - self.start_time

    def get_return(self):
        return self.ret


T = parameter.test_num
solvers = [Constrain_Programing.solve, DCFlow.solve]
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
        graders.append(g)
    # chuyen phan thread join re ngoai
    for g in graders:
        g.join()
        print('time:', g.get_time())
        a = g.get_return()
        if a is None:
            print('failed')
        else:
            print(a[0])
            for i in a[1]:
                print(i)
