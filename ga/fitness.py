import math
from ga.chromosome import decode_routes

def euclid(a, b):
    """Euclidean distance between two points (x, y)."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def fitness(individual, depot, customers, vehicles):
    """Compute total distance of all vehicle routes (lower is better)."""
    routes = decode_routes(individual, vehicles)
    total = 0
    for r in routes:
        if not r: 
            continue
        total += euclid(depot, customers[r[0]])  # depot -> first
        for i in range(len(r) - 1):              # customer -> customer
            total += euclid(customers[r[i]], customers[r[i+1]])
        total += euclid(customers[r[-1]], depot) # last -> depot
    return total
