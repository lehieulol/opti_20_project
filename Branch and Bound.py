import math


def solve(_N, _M, _K, _linked):
    """
    :param _N:
    :param _M:
    :param _K:
    :param _linked: type edge list
    :return:
    """
    count_n = []
    count_m = []
    picked = []
    for i in range(_N + 1):
        count_n.append(0)
    for _ in range(_M + 1):
        count_m.append(0)
    for _ in _linked:
        picked.append(0)

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
        count_n[_linked[current][0]] += 1
        count_m[_linked[current][1]] += 1
        picked[current] = 1
        backtrack(current + 1)
        count_n[_linked[current][0]] -= 1
        count_m[_linked[current][1]] -= 1
        picked[current] = 0
        backtrack(current + 1)

    backtrack(0)
    return _min, min_picked

