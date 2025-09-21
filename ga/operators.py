import random
from typing import List

def order_crossover(p1: List[int], p2: List[int], rng: random.Random) -> List[int]:
    N = len(p1)
    if N <= 2:
        return p1[:] if rng.random() < 0.5 else p2[:]
    
    # Select crossover points
    a, b = sorted(rng.sample(range(N), 2))
    
    # Create child with selected segment from p1
    child = [None] * N
    child[a:b+1] = p1[a:b+1]  # Fixed: include endpoint
    
    # Fill remaining positions with p2 in order
    p2_filtered = [x for x in p2 if x not in child[a:b+1]]
    
    # Fill positions before crossover segment
    fill_idx = 0
    for i in range(a):
        child[i] = p2_filtered[fill_idx]
        fill_idx += 1
    
    # Fill positions after crossover segment
    for i in range(b+1, N):
        child[i] = p2_filtered[fill_idx]
        fill_idx += 1
    
    return child

def cuts_crossover(c1: List[int], c2: List[int], N: int, V: int, rng: random.Random) -> List[int]:
    if V <= 2:
        point = 1
    else:
        point = rng.randint(1, V-2)
    child = c1[:point] + c2[point:]
    child = sorted(set([x for x in child if 1 <= x < N]))
    while len(child) < V-1:
        val = rng.randint(1, N-1)
        if val not in child:
            child.append(val)
    child.sort()
    return child

def swap_mutation_perm(perm: List[int], pm: float, rng: random.Random):
    for i in range(len(perm)):
        if rng.random() < pm:
            j = rng.randint(0, len(perm)-1)
            perm[i], perm[j] = perm[j], perm[i]

def jitter_mutation_cuts(cuts: List[int], pm: float, N: int, rng: random.Random):
    for i in range(len(cuts)):
        if rng.random() < pm:
            delta = rng.randint(-1, 1)
            cuts[i] = min(max(1, cuts[i]+delta), N-1)
    cuts.sort()
def route_aware_mutation(individual, pm: float, N: int, V: int, rng: random.Random):
    """Route-aware mutation that can move customers between routes"""
    from .chromosome import decode_routes, Individual
    
    if rng.random() < pm:
        routes = decode_routes(individual, V)
        non_empty_routes = [i for i, route in enumerate(routes) if route]
        
        if len(non_empty_routes) >= 2:
            # Move customer between routes
            source_idx = rng.choice(non_empty_routes)
            target_idx = rng.randint(0, V-1)
            
            if routes[source_idx]:  # Ensure source route is not empty
                # Remove customer from source route
                customer_pos = rng.randint(0, len(routes[source_idx])-1)
                customer = routes[source_idx].pop(customer_pos)
                
                # Add to target route
                insert_pos = rng.randint(0, len(routes[target_idx]))
                routes[target_idx].insert(insert_pos, customer)
                
                # Convert back to permutation + cuts format
                new_perm = []
                new_cuts = []
                current_pos = 0
                
                for route in routes:
                    if route:
                        new_perm.extend(route)
                        current_pos += len(route)
                        if current_pos < N:  # Don't add cut after last route
                            new_cuts.append(current_pos)
                
                # Ensure we have exactly V-1 cuts
                while len(new_cuts) < V-1 and len(new_cuts) > 0:
                    new_cuts.append(min(N-1, max(new_cuts) + 1))
                new_cuts = new_cuts[:V-1]  # Trim if too many
                new_cuts.sort()
                
                # Update individual
                individual.perm = new_perm
                individual.cuts = new_cuts