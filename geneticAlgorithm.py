import numpy as np
import time


class alg_gen:
    def __init__(self, n, T=100, scale=10, n_pop=1000, k = 10, cross_prob=0.9, mutation_prob=0.01):
        self.n_ = n
        self.T_ = T
        self.scale_ = scale
        self.v, self.c, self.C = self.random_dkp()
        self.chromosom = np.zeros((n_pop, n))
        self.n_pop_ = n_pop
        self.k = k
        self.cross_prob = cross_prob
        self.mutation_prob = mutation_prob


    def random_dkp(self):
        items = np.ceil(np.random.rand(self.n_, 2) * self.scale_)
        C = int(np.ceil(0.5 * 0.5 * self.n_ * self.scale_))
        v = items[:, 0]
        c = items[:, 1]
        return v, c, C

    def funkcja_przystosowania(self, chr):
        if np.sum(self.c[chr == 1]) <= self.C:
            return np.sum(self.v[chr == 1])
        else:
            return 0

    def populacja_poczatkowa(self):
        prawdopodobienstwo = 0.1
        for i in range(self.n_pop_):
            for j in range(self.n_):
                if np.random.rand() <= prawdopodobienstwo:
                    self.chromosom[i][j] = 1

    def main_alg(self):
        for i in range(self.T_):
            chromosom_new = []
            ocena = np.zeros(self.n_pop_)
            for j in range(self.n_pop_):
                ocena[j] = self.funkcja_przystosowania(self.chromosom[j])

            for j in range(self.n_pop_):  # selekcja turniejowa
                los = self.los_bez_powt()
                best_ocena = 0
                for k in range(self.k):
                    if best_ocena < ocena[los[k]]:
                        best_ocena = ocena[los[k]]
                        best_ocena_index = los[k]
                not_best = los[np.random.randint(self.k)]
                while best_ocena == not_best:
                    not_best = los[np.random.randint(self.k)]
                if np.random.rand() <= 0.9:
                    chromosom_new.append(self.chromosom[best_ocena_index])
                else:
                    chromosom_new.append(self.chromosom[not_best])

            self.chromosom = chromosom_new

            self.crossover()
            self.mutation()
        best_ocena = 0
        for i in range(self.n_pop_):
            ocena[i] = self.funkcja_przystosowania(self.chromosom[i])
            if ocena[i] > best_ocena:
                best_ocena = ocena[i]
                best_ocena_index = i
            return self.chromosom[best_ocena_index]



    def crossover(self): # krzyżowanie jednopunktowe
        cross_point = np.random.randint(1, self.n_)
        for j in range(int(self.n_pop_ / 2)):
            if np.random.rand() >= self.cross_prob:
                continue
            else:
                temp1 = self.chromosom[j][:cross_point]
                temp1 = np.append(temp1, (self.chromosom[int(j + self.n_pop_/2)][cross_point:]))
                temp2 = self.chromosom[int(j + self.n_pop_/2)][:cross_point]
                temp2 = np.append(temp2, (self.chromosom[j][cross_point:]))
                self.chromosom[j] = temp1
                self.chromosom[int(j + self.n_pop_/2)] = temp2

    def mutation(self):
        for j in range(self.n_pop_):
            if np.random.rand() <= self.mutation_prob:
                mutation_index = np.random.randint(self.n_)
                if self.chromosom[j][mutation_index] == 0:
                    self.chromosom[j][mutation_index] = 1
                else:
                    self.chromosom[j][mutation_index] = 0

    def los_bez_powt(self):
        bylo = []
        tab = []
        for i in range(self.k):
            los = np.random.randint(self.n_pop_)
            while los in bylo:
                los = np.random.randint(self.n_pop_)
                bylo.append(los)
            tab.append(los)
        return tab


if __name__ == "__main__":
    np.random.seed(6)
    n = 10
    algorytm = alg_gen(n, 100)
    algorytm.populacja_poczatkowa()

    t1 = time.time()
    best_pack = algorytm.main_alg()
    t2 = time.time()
    print("best pack: " + str(algorytm.v[best_pack == 1]))
    print("capacity used: " + str(algorytm.c[best_pack == 1].sum()))
    '''
    t1 = time.time()
    best_pack, solution = solve_dkp_exact(v, c, C)
    t2 = time.time()
    print("BEST_PACK: " + str(best_pack))
    print("CAPACITY USED: " + str((solution * c).sum()))'''
    print("TIME: " + str(t2 - t1))
    print(algorytm.v)
