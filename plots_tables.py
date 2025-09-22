import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Tuple

def plot_routes_matplotlib(best_ind, customers_list, depot, n_vehicles, title="", filename=None):
    """
    customers_list: [(x,y), ...] in the same order used to build dmat (0..N-1)
    best_ind: Individual with perm containing indices referring to customers_list positions (1..N)
    """
    from ga.chromosome import decode_routes
    routes = decode_routes(best_ind, n_vehicles)
    xs = [c[0] for c in customers_list]
    ys = [c[1] for c in customers_list]
    plt.figure(figsize=(7,7))
    plt.scatter(xs, ys, label="customers", zorder=3)
    plt.scatter([depot[0]], [depot[1]], color="red", s=120, marker="*", label="depot", zorder=4)

    for r in routes:
        if not r:
            continue
        # Convert 1-based indices to 0-based for plotting
        r_zero_based = [i-1 for i in r]
        xs_path = [depot[0]] + [customers_list[i][0] for i in r_zero_based] + [depot[0]]
        ys_path = [depot[1]] + [customers_list[i][1] for i in r_zero_based] + [depot[1]]
        plt.plot(xs_path, ys_path, linewidth=1.5, alpha=0.85)

    plt.title(title)
    plt.legend()
    plt.axis("equal")
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.close()


def plot_convergence_histories(histories: List[List[float]], title="", filename=None):
    """
    histories: list of lists (best distance per generation) for multiple runs
    """
    plt.figure(figsize=(8,5))
    for h in histories:
        plt.plot(h, alpha=0.25, color="gray")
    # pad to same length
    max_len = max(len(h) for h in histories)
    arr = np.vstack([np.array(h + [h[-1]]*(max_len-len(h))) for h in histories])
    mean_curve = arr.mean(axis=0)
    plt.plot(mean_curve, color="C0", linewidth=2.5, label="Mean")
    plt.xlabel("Generation")
    plt.ylabel("Best Distance")
    plt.title(title)
    plt.legend()
    plt.grid(True)
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.close()

def plot_instance_metric(df_results: pd.DataFrame, metric: str, filename=None, title=None):
    """
    df_results: DataFrame with columns ['Instance','ParamSet', metric]
    metric: e.g. 'MeanRuntime' or 'MeanDist'
    Produces a line plot across instances for each ParamSet
    """
    palette = sns.color_palette("Dark2", df_results['ParamSet'].nunique())
    plt.figure(figsize=(8,4))
    for i, (name, group) in enumerate(df_results.groupby("ParamSet")):
        xs = group['Instance'].values
        ys = group[metric].values
        plt.plot(xs, ys, marker='o', label=name)
    plt.xlabel("Instance")
    plt.ylabel(metric)
    plt.title(title or f"{metric} per Instance")
    plt.legend()
    plt.grid(True)
    if filename:
        plt.savefig(filename, bbox_inches='tight')
    plt.close()
