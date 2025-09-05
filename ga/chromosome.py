import random

def create_individual(customers):
    """
    Create a random permutation of customer IDs.
    This is the chromosome representation.
    """
    return random.sample(list(customers.keys()), len(customers))

def decode_routes(individual, num_vehicles):
    """
    Split a customer permutation into 'num_vehicles' routes.
    Ensures nearly equal number of customers per vehicle.
    """
    n = len(individual)
    base = n // num_vehicles
    rem = n % num_vehicles

    sizes = [base + (1 if i < rem else 0) for i in range(num_vehicles)]

    routes = []
    idx = 0
    for s in sizes:
        routes.append(individual[idx:idx+s])
        idx += s

    return routes
