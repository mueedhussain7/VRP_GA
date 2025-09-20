import random
from typing import List

class Individual:
    def __init__(self, perm: List[int], cuts: List[int]):
        self.perm = perm
        self.cuts = cuts

def random_individual(N: int, V: int, rng: random.Random) -> Individual:
    perm = list(range(1, N+1))
    rng.shuffle(perm)
    cuts = sorted(rng.sample(range(1, N), V-1)) if V > 1 else []
    return Individual(perm, cuts)


def decode_routes(ind: Individual, n_vehicles: int) -> List[List[int]]:
    routes = []
    prev = 0
    cuts = ind.cuts + [len(ind.perm)]
    for c in cuts:
        routes.append(ind.perm[prev:c])
        prev = c
    return routes
