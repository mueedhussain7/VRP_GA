import random
from typing import List, Tuple
from .chromosome import Individual, random_individual, decode_routes
from .operators import order_crossover, cuts_crossover, swap_mutation_perm, jitter_mutation_cuts
from .fitness import total_distance

def genetic_algorithm(dmat: "np.ndarray", N: int, V: int,
                      pop_size: int, generations: int, k_tourn: int,
                      pc: float, pm_perm: float, pm_cuts: float,
                      seed: int = None, log_convergence: bool = False
                     ) -> Tuple[Individual, float, List[float]]:

    rng = random.Random(seed)
    pop = [random_individual(N, V, rng) for _ in range(pop_size)]
    histories = []

    def tournament(pop):
        best = rng.choice(pop)
        for _ in range(k_tourn-1):
            ind = rng.choice(pop)
            if total_distance(ind, dmat, V) < total_distance(best, dmat, V):
                best = ind
        return best

    for gen in range(generations):
        new_pop = []
        for _ in range(pop_size // 2):
            p1, p2 = tournament(pop), tournament(pop)
            if rng.random() < pc:
                child_perm = order_crossover(p1.perm, p2.perm, rng)
                child_cuts = cuts_crossover(p1.cuts, p2.cuts, N, V, rng)
            else:
                child_perm = p1.perm[:]
                child_cuts = p1.cuts[:]
            swap_mutation_perm(child_perm, pm_perm, rng)
            jitter_mutation_cuts(child_cuts, pm_cuts, N, rng)
            new_pop.append(Individual(child_perm, child_cuts))
            new_pop.append(Individual(child_perm[:], child_cuts[:]))
        pop = new_pop[:pop_size]  # maintain population size
        if log_convergence:
            best_dist = min(total_distance(ind, dmat, V) for ind in pop)
            histories.append(best_dist)

    best_ind = min(pop, key=lambda ind: total_distance(ind, dmat, V))
    best_dist = total_distance(best_ind, dmat, V)
    return best_ind, best_dist, histories
