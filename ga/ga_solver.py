import random
import math
from ga.chromosome import create_individual, decode_routes
from ga.fitness import fitness
from ga.operators import crossover, mutate

def solve_qiea(instance, pop_size=50, generations=100, delta_theta=0.05, seed=None):
    """
    Quantum-Inspired Evolutionary Algorithm (QIEA) for VRP.

    Parameters:
        instance: dict with 'DEPOT', 'CUSTOMERS', 'VEHICLES'
        pop_size: population size
        generations: number of generations
        delta_theta: rotation angle for QIEA update
        seed: random seed for reproducibility

    Returns:
        best_individual: permutation of customers
        best_cost: total route distance
        best_routes: decoded vehicle routes
        best_cost_per_gen: list of best cost per generation
    """
    if seed is not None:
        random.seed(seed)

    depot = instance["DEPOT"]
    customers = instance["CUSTOMERS"]
    num_vehicles = instance["VEHICLES"]
    n = len(customers)

    # Initialize quantum population as probability amplitudes (each gene has 0.5 probability for each state)
    q_population = [[0.5 for _ in range(n)] for _ in range(pop_size)]

    # Classical population decoded from quantum states
    def measure(q_individual):
        """Measure quantum individual to classical permutation."""
        # Create permutation by sorting based on probabilities + randomness
        indices = list(range(n))
        probs = q_individual[:]
        # Add small random noise to avoid ties
        noisy_probs = [p + random.random()*1e-3 for p in probs]
        # Sort indices based on noisy probability
        sorted_indices = [x for _, x in sorted(zip(noisy_probs, indices), reverse=True)]
        return sorted_indices

    population = [measure(q) for q in q_population]
    fitnesses = [fitness(ind, depot, customers, num_vehicles) for ind in population]

    # Track best individual
    best_ind = min(zip(population, fitnesses), key=lambda x: x[1])
    best_cost_per_gen = []

    for gen in range(generations):
        # Update quantum individuals using rotation inspired by classical GA result
        for i in range(pop_size):
            # Compare with best and rotate probabilities
            for j in range(n):
                if population[i][j] != best_ind[0][j]:
                    # Rotate probability towards best
                    if population[i][j] < best_ind[0][j]:
                        q_population[i][j] += delta_theta
                    else:
                        q_population[i][j] -= delta_theta
                    # Keep probability in [0,1]
                    q_population[i][j] = min(max(q_population[i][j], 0.0), 1.0)

        # Measure to get new classical population
        population = [measure(q) for q in q_population]

        # Apply classical GA operators
        new_population = []
        while len(new_population) < pop_size:
            # Tournament selection
            candidates = random.sample(list(zip(population, fitnesses)), 3)
            parent1 = min(candidates, key=lambda x: x[1])[0]

            candidates = random.sample(list(zip(population, fitnesses)), 3)
            parent2 = min(candidates, key=lambda x: x[1])[0]

            # Crossover
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)

            # Mutation
            child1 = mutate(child1, pm=0.1)
            child2 = mutate(child2, pm=0.1)

            new_population.extend([child1, child2])

        population = new_population[:pop_size]
        fitnesses = [fitness(ind, depot, customers, num_vehicles) for ind in population]

        # Track generation best
        gen_best = min(zip(population, fitnesses), key=lambda x: x[1])
        best_cost_per_gen.append(gen_best[1])

        if gen_best[1] < best_ind[1]:
            best_ind = gen_best

    best_individual, best_cost = best_ind
    best_routes = decode_routes(best_individual, num_vehicles)
    return best_individual, best_cost, best_routes, best_cost_per_gen
