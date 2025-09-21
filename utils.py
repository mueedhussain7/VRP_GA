import numpy as np
from typing import Dict, List, Tuple

def customers_to_ordered_list(customers_dict: Dict[int, Tuple[float, float]]):
    """
    Convert customers dict (id -> (x,y)) to a deterministic ordered list.
    Returns (sorted_keys, customers_list) where customers_list[i] corresponds to sorted_keys[i].
    """
    sorted_keys = sorted(customers_dict.keys())
    customers_list = [customers_dict[k] for k in sorted_keys]
    return sorted_keys, customers_list

def distance_matrix(depot: Tuple[float,float], customers_list: List[Tuple[float,float]]):
    """
    Build numpy (N+1)x(N+1) distance matrix where index 0 = depot, 1..N = customers in customers_list order.
    """
    pts = [tuple(depot)] + [tuple(c) for c in customers_list]
    n = len(pts)
    dmat = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i == j:
                dmat[i, j] = 0.0
            else:
                dx = pts[i][0] - pts[j][0]
                dy = pts[i][1] - pts[j][1]
                dmat[i, j] = (dx*dx + dy*dy) ** 0.5
    return dmat
