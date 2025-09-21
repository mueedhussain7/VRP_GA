import random
from typing import List, Tuple
from .chromosome import Individual, random_individual, decode_routes
from .operators import order_crossover, cuts_crossover, swap_mutation_perm, jitter_mutation_cuts, route_aware_mutation
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

    for gen in range(generations):  # This line should be here
        new_pop = []
        
        # Create offspring pairs 
        for _ in range(pop_size // 2):
            p1, p2 = tournament(pop), tournament(pop)
            
            # Ensure parents are different
            attempts = 0
            while p1 is p2 and attempts < 5:
                p2 = tournament(pop)
                attempts += 1
            
            # Create two children
            if rng.random() < pc:
                child1_perm = order_crossover(p1.perm, p2.perm, rng)
                child1_cuts = cuts_crossover(p1.cuts, p2.cuts, N, V, rng)
                
                child2_perm = order_crossover(p2.perm, p1.perm, rng)
                child2_cuts = cuts_crossover(p2.cuts, p1.cuts, N, V, rng)
            else:
                child1_perm = p1.perm[:]
                child1_cuts = p1.cuts[:]
                child2_perm = p2.perm[:]
                child2_cuts = p2.cuts[:]
            
            # Apply mutations
            swap_mutation_perm(child1_perm, pm_perm, rng)
            jitter_mutation_cuts(child1_cuts, pm_cuts, N, rng)
            child1 = Individual(child1_perm, child1_cuts)
            route_aware_mutation(child1, pm_perm * 0.5, N, V, rng)
            
            swap_mutation_perm(child2_perm, pm_perm, rng)
            jitter_mutation_cuts(child2_cuts, pm_cuts, N, rng)
            child2 = Individual(child2_perm, child2_cuts)
            route_aware_mutation(child2, pm_perm * 0.5, N, V, rng)
            
            new_pop.append(child1)
            new_pop.append(child2)
        
        # Handle odd population size
        if len(new_pop) < pop_size:
            p1 = tournament(pop)
            new_pop.append(Individual(p1.perm[:], p1.cuts[:]))
        
        # Elitism - keep best individual from previous generation
        if gen > 0:
            current_best = min(pop, key=lambda ind: total_distance(ind, dmat, V))
            # Replace worst individual in new population
            worst_idx = max(range(len(new_pop)), 
                           key=lambda i: total_distance(new_pop[i], dmat, V))
            new_pop[worst_idx] = current_best
        
        pop = new_pop[:pop_size]  # maintain population size

        
        if log_convergence:
            best_dist = min(total_distance(ind, dmat, V) for ind in pop)
            histories.append(best_dist)


    best_ind = min(pop, key=lambda ind: total_distance(ind, dmat, V))
    best_dist = total_distance(best_ind, dmat, V)
    return best_ind, best_dist, histories