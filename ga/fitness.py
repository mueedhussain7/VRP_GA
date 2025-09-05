import math
from ga.chromosome import decode_routes

def euclidean(a, b):
    """Compute Euclidean distance between two points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def fitness(individual, depot, customers, num_vehicles):
    """
    Compute total route distance for a GA individual.
    Lower distance = better fitness.
    """
    routes = decode_routes(individual, num_vehicles)
    total_distance = 0

    for r in routes:
        if not r:
            continue
        # Depot -> first customer
        total_distance += euclidean(depot, customers[r[0]])
        # Customer -> customer
        for i in range(len(r) - 1):
            total_distance += euclidean(customers[r[i]], customers[r[i+1]])
        # Last customer -> depot
        total_distance += euclidean(customers[r[-1]], depot)

    return total_distance
