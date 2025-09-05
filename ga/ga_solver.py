import random
from ga.chromosome import create_individual, decode_routes
from ga.fitness import fitness
from ga.operators import crossover, mutate

def tournament_selection(population, fitnesses, k=3):
    """Pick the best of k random individuals."""
    candidates = random.sample(list(zip(population, fitnesses)), k)
    return min(candidates, key=lambda x: x[1])[0]

def solve_ga(instance, pop_size=50, generations=100, pc=0.8, pm=0.1):
    depot = instance["DEPOT"]
    customers = instance["CUSTOMERS"]
    vehicles = instance["VEHICLES"]

    # Initialize population
    population = [create_individual(customers) for _ in range(pop_size)]
    fitnesses = [fitness(ind, depot, customers, vehicles) for ind in population]

    best_ind = min(zip(population, fitnesses), key=lambda x: x[1])
    best_cost_per_gen = []

    for _ in range(generations):
        new_pop = []
        while len(new_pop) < pop_size:
            p1 = tournament_selection(population, fitnesses)
            p2 = tournament_selection(population, fitnesses)
            if random.random() < pc:
                c1 = crossover(p1, p2)
                c2 = crossover(p2, p1)
            else:
                c1, c2 = p1[:], p2[:]
            new_pop.extend([mutate(c1, pm), mutate(c2, pm)])
        
        population = new_pop[:pop_size]
        fitnesses = [fitness(ind, depot, customers, vehicles) for ind in population]

        gen_best = min(zip(population, fitnesses), key=lambda x: x[1])
        best_cost_per_gen.append(gen_best[1])

        if gen_best[1] < best_ind[1]:
            best_ind = gen_best

    best_individual, best_cost = best_ind
    best_routes = decode_routes(best_individual, vehicles)

    return best_individual, best_cost, best_routes, best_cost_per_gen
