import math
from utils import ELtoM

def solve(_N, _M, _K, _linked):
    """
    :param _N:
    :param _M:
    :param _K:
    :param _linked: type edge list
    :return:
    """
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
        if current >= len(_linked) - 1:
            min_picked.clear()
            min_picked.extend(picked)
            _min = max(count_m)
            return
        count_n[_linked[current][0]] += 1
        count_m[_linked[current][1]] += 1
        picked[current] = 1
        backtrack(current + 1)
        count_n[_linked[current][0]] -= 1
        count_m[_linked[current][1]] -= 1
        picked[current] = 0
        backtrack(current + 1)

    backtrack(0)
    return _min, ELtoM(_N, _M, edge_list=_linked, picked=min_picked)

