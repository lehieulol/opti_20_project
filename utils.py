def get_input(filename, linked_type='edge list'):
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
            a = map(int,a)
            for _ in a:
                linked.append((i+1,_))
    else:
        raise ValueError
    print(linked)
    f.close()
    return N, M, K, linked
