import random
from typing import List

def order_crossover(p1: List[int], p2: List[int], rng: random.Random) -> List[int]:
    N = len(p1)
    a, b = sorted(rng.sample(range(N), 2))
    child = [None]*N
    child[a:b] = p1[a:b]
    fill = [x for x in p2 if x not in child]
    j = 0
    for i in range(N):
        if child[i] is None:
            child[i] = fill[j]
            j += 1
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
