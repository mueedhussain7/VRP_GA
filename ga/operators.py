import random

def crossover(parent1, parent2):
    """
    Ordered Crossover (OX) for permutation chromosomes.
    Returns a child permutation.
    """
    n = len(parent1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n

    # Copy segment from parent1
    child[a:b+1] = parent1[a:b+1]

    # Fill remaining positions from parent2 in order
    p2_items = [x for x in parent2 if x not in child]
    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = p2_items[j]
            j += 1

    return child

def mutate(individual, pm):
    """
    Swap mutation: with probability pm, swap two random genes.
    """
    n = len(individual)
    for i in range(n):
        if random.random() < pm:
            j = random.randrange(n)
            individual[i], individual[j] = individual[j], individual[i]
    return individual
