import random
import math 
from ga_vrp_instances import SMALL_INSTANCE_1, MEDIUM_INSTANCE_1, LARGE_INSTANCE_1


# Problem setup: VRP

INSTANCE = SMALL_INSTANCE_1

DEPOT = INSTANCE["DEPOT"]
CUSTOMERS = INSTANCE["CUSTOMERS"]
VEHICLES = INSTANCE["VEHICLES"]
     # Number of vehicles available for delivery

POPULATION_SIZE = 6  # Number of candidate solutions in the GA population
GENERATIONS = 5      # Number of generations the GA will evolve

# Helper functions
def euclid(a, b):
    """Compute Euclidean distance between two points a and b 
    Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)"""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def decode_routes(individual, k=VEHICLES):
    n = len(individual)       
    base = n // k             
    rem = n % k             
    sizes = [base + (1 if i < rem else 0) for i in range(k)]

    routes = [] 
    idx = 0   

    for s in sizes:
        routes.append(individual[idx:idx+s])
        idx += s   

    return routes 

# GA functions
def create_individual():
    return random.sample(list(CUSTOMERS.keys()), len(CUSTOMERS))

def fitness(individual):
    routes = decode_routes(individual)
    total = 0
    for r in routes:
        if not r:  
            continue
        total += euclid(DEPOT, CUSTOMERS[r[0]])  
        for i in range(len(r)-1):
            total += euclid(CUSTOMERS[r[i]], CUSTOMERS[r[i+1]])  
        total += euclid(CUSTOMERS[r[-1]], DEPOT) 
    
    # Avoid divide by zero (just in case)
    return 1 / total if total > 0 else 0  

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [-1] * len(parent1)    
    child[start:end] = parent1[start:end] 
    pointer = end
    for cust in parent2:
        if cust not in child: 
            child[pointer] = cust
            pointer = (pointer + 1) % len(child) 
    # Replace any leftover -1 with random unused customers (safety)
    for i in range(len(child)):
        if child[i] == -1:
            for cust in parent2:
                if cust not in child:
                    child[i] = cust
                    break
    return child

def mutate(individual, rate=0.1):
    if random.random() < rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

def visualize_individual(individual):
    routes = decode_routes(individual)
    return " | ".join(str(r) for r in routes)

# Main GA loop
def genetic_algorithm():

    population = [create_individual() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        print(f"\nGeneration {gen}:")
        for i, ind in enumerate(population):
            print(f"Individual {i}: {visualize_individual(ind)}, Fitness: {fitness(ind):.6f}")

        # Generate next population
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            parent1, parent2 = random.sample(population, 2) 
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])
        population = new_population[:POPULATION_SIZE] 

    # Final population
    print("\nFinal Population:")
    for i, ind in enumerate(population):
        print(f"Individual {i}: {visualize_individual(ind)}, Fitness: {fitness(ind):.6f}")

# Run the GA
if __name__ == "__main__":
    genetic_algorithm()
