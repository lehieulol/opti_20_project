def solve(N, M, K, linked):
    def eval(bit_array):
        count_n = [0 for _ in range(N)]
        count_m = [0 for _ in range(M)]
        for i in len(bit_array):
            if bit_array[i]:
                count_n[linked[i][0] - 1] += 1
                count_m[linked[i][1] - 1] += 1
        if min(count_n) < K:
            return float('-inf')
        return max(count_m)

    def crossover(bit_array_1, bit_array_2):
        pass

    def mutation(bit_array_1):
        pass
    
    def selection():
        pass