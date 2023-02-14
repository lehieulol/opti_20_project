import math
import time
import parameter

from utils import ELtoM


def solve(_N, _M, _K, _linked):
    """
    :param _N:
    :param _M:
    :param _K:
    :param _linked: type edge list
    :return:
    """
    start_time = time.time()

    count_n = [0 for i in range(_N + 1)]
    count_m = [0 for i in range(_M + 1)]
    picked = [0 for i in _linked]

    _linked = _linked+[(_N+1, 0)]

    _min = math.inf
    min_picked = []

    def backtrack(current):
        nonlocal _min
        nonlocal min_picked
        if _linked[current][0] > 1 and count_n[_linked[current][0] - 1] < _K:
            return
        # cutoff if there is no better solution
        if max(count_m) >= _min:
            return
        if current >= len(_linked) - 1:
            min_picked.clear()
            min_picked.extend(picked)
            _min = max(count_m)
            return
        if time.time() - start_time > parameter.wait - 1:
            raise TimeoutError
        count_n[_linked[current][0]] += 1
        count_m[_linked[current][1]] += 1
        picked[current] = 1
        backtrack(current + 1)
        count_n[_linked[current][0]] -= 1
        count_m[_linked[current][1]] -= 1
        picked[current] = 0
        backtrack(current + 1)
    try:
        backtrack(0)
    finally:
        if _min != float('inf'):
            return _min, ELtoM(_N, _M, edge_list=_linked, picked=min_picked)
        else:
            return None


