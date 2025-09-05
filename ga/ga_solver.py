import random
from ga.chromosome import create_individual, decode_routes
from ga.fitness import fitness
from ga.operators import crossover, mutate

def tournament_selection(population, fitnesses, k=3):
    """
    Select the best individual among k random candidates.
    """
    candidates = random.sample(list(zip(population, fitnesses)), k)
    return min(candidates, key=lambda x: x[1])[0]

def solve_ga(instance, pop_size=50, generations=100, pc=0.8, pm=0.1, seed=None):
    """
    Run GA to solve a VRP instance.
    
    Returns:
        best_individual: permutation of customers
        best_cost: total route distance
        best_routes: decoded routes for vehicles
        best_cost_per_gen: list of best fitness per generation
    """
    if seed is not None:
        random.seed(seed)

    depot = instance["DEPOT"]
    customers = instance["CUSTOMERS"]
    num_vehicles = instance["VEHICLES"]

    # Initialize population
    population = [create_individual(customers) for _ in range(pop_size)]
    fitnesses = [fitness(ind, depot, customers, num_vehicles) for ind in population]

    # Track best individual overall
    best_ind = min(zip(population, fitnesses), key=lambda x: x[1])
    best_cost_per_gen = []

    for gen in range(generations):
        new_population = []

        # Generate new population
        while len(new_population) < pop_size:
            # Selection
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)

            # Crossover
            if random.random() < pc:
                child1 = crossover(parent1, parent2)
                child2 = crossover(parent2, parent1)
            else:
                child1, child2 = parent1[:], parent2[:]

            # Mutation
            new_population.append(mutate(child1, pm))
            new_population.append(mutate(child2, pm))

        # Trim to population size
        population = new_population[:pop_size]
        fitnesses = [fitness(ind, depot, customers, num_vehicles) for ind in population]

        # Track generation best
        gen_best = min(zip(population, fitnesses), key=lambda x: x[1])
        best_cost_per_gen.append(gen_best[1])

        # Update overall best
        if gen_best[1] < best_ind[1]:
            best_ind = gen_best

    best_individual, best_cost = best_ind
    best_routes = decode_routes(best_individual, num_vehicles)

    return best_individual, best_cost, best_routes, best_cost_per_gen
