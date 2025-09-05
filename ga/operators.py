import random

def crossover(parent1, parent2):
    """Ordered crossover (OX)."""
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [-1] * len(parent1)
    child[start:end] = parent1[start:end]
    pointer = end
    for cust in parent2:
        if cust not in child:
            child[pointer] = cust
            pointer = (pointer + 1) % len(child)
    return child

def mutate(individual, rate=0.1):
    """Swap mutation."""
    if random.random() < rate:
        i, j = random.sample(range(len(individual)), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual
