import random

def create_individual(customers):
    """Create a random permutation of customers (chromosome)."""
    return random.sample(list(customers.keys()), len(customers))

def decode_routes(individual, k):
    """Split customer permutation into k vehicle routes (nearly even split)."""
    n = len(individual)
    base = n // k
    rem = n % k
    sizes = [base + (1 if i < rem else 0) for i in range(k)]
    
    routes, idx = [], 0
    for s in sizes:
        routes.append(individual[idx:idx+s])
        idx += s
    return routes
