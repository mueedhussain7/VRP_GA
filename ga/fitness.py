from ga.chromosome import decode_routes, Individual
from typing import List
import numpy as np

def route_distance(route: List[int], dmat: np.ndarray) -> float:
    if not route:
        return 0
    total = dmat[0, route[0]]  # depot to first
    for i in range(len(route)-1):
        total += dmat[route[i], route[i+1]]
    total += dmat[route[-1], 0]  # return to depot
    return total

def total_distance(ind: Individual, dmat: np.ndarray, V: int) -> float:
    routes = decode_routes(ind, V)
    return sum(route_distance(r, dmat) for r in routes)

def fitness(ind: Individual, dmat: np.ndarray, V: int) -> float:
    return -total_distance(ind, dmat, V)  # GA maximizes fitness
