def get_input(filename, linked_type='edge list'):
    """

    :param filename:
    :param linked_type:
    'adjacency list'
    'edge list'
    'matrix' (not implemented)
    :return:
    """
    f = open(filename)
    N, M, K = map(int, f.readline().split())
    print(N, M, K)
    linked = []
    if linked_type == 'adjacency list':
        for i in range(N):
            linked.append(f.readline().split())
            linked[-1].pop(0)
            linked[-1] = list(map(int, linked[-1]))
    elif linked_type == 'edge list':
        for i in range(N):
            a = f.readline().split()
            a.pop(0)
            a = map(int, a)
            for _ in a:
                linked.append((i + 1, _))
    else:
        raise ValueError
    print(linked)
    f.close()
    return N, M, K, linked


def ELtoM(N, M, edge_list, picked):
    matrix = [['.' for _ in range(M)] for _ in range(N)]
    for _ in range(len(picked)):
        if picked[_] == 1:
            matrix[edge_list[_][0]-1][edge_list[_][1]-1] = '#'
    return matrix
