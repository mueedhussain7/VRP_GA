import os, shutil, time, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ga.ga_solver import genetic_algorithm
from utils import customers_to_ordered_list, distance_matrix
from plots_tables import plot_routes_matplotlib, plot_convergence_histories, plot_instance_metric
from data.small_instances import SMALL_INSTANCE_1, SMALL_INSTANCE_2
from data.medium_instances import MEDIUM_INSTANCE_1, MEDIUM_INSTANCE_2
from data.large_instances import LARGE_INSTANCE_1, LARGE_INSTANCE_2

# ---------------- prepare results folder ----------------
RESULTS_DIR = "results"
if os.path.exists(RESULTS_DIR):
    shutil.rmtree(RESULTS_DIR)
os.makedirs(RESULTS_DIR, exist_ok=True)

# ---------------- experiment config ----------------
param_sets = {
    "Standard": {"pop_size": 80, "generations": 300, "k_tourn":3, "pc":0.8, "pm_perm":0.02, "pm_cuts":0.08},
    "Large_Scale": {"pop_size":150, "generations":500, "k_tourn":3, "pc":0.85, "pm_perm":0.05, "pm_cuts":0.15},
    "compact": {"pop_size":30, "generations":200, "k_tourn":5, "pc":0.7, "pm_perm":0.008, "pm_cuts":0.3}
}
N_RUNS = 15
INSTANCES = [
    ("Small-1", SMALL_INSTANCE_1), ("Small-2", SMALL_INSTANCE_2),
    ("Medium-1", MEDIUM_INSTANCE_1), ("Medium-2", MEDIUM_INSTANCE_2),
    ("Large-1", LARGE_INSTANCE_1), ("Large-2", LARGE_INSTANCE_2),
]

# ---------------- safety check: vehicles <= customers ----------------
for name, inst in INSTANCES:
    n_customers = len(inst["CUSTOMERS"])
    v = inst["VEHICLES"]
    if v > n_customers:
        raise ValueError(f"Instance {name}: VEHICLES ({v}) > number of customers ({n_customers}). Fix data.")

# ---------------- run experiments ----------------
results = []
for inst_id, (inst_name, inst) in enumerate(INSTANCES, start=1):
    depot = inst["DEPOT"]
    cust_keys, customers_list = customers_to_ordered_list(inst["CUSTOMERS"])
    N = len(customers_list)
    V = inst["VEHICLES"]
    dmat = distance_matrix(depot, customers_list)  # numpy (N+1)x(N+1), 0 = depot, 1..N customers

    print(f"\n=== Instance {inst_name}: N={N}, V={V} ===")

    for set_name, params in param_sets.items():
        print(f"  ParamSet: {set_name} -> {params}")
        dists = []
        times = []
        histories_all = []
        best_inds = []

        for seed in range(N_RUNS):
            start_time = time.time()
            # genetic_algorithm expects dmat and N
            best_ind, best_dist, best_hist = genetic_algorithm(
                dmat=dmat,
                N=N,
                V=V,
                pop_size=params["pop_size"],
                generations=params["generations"],
                k_tourn=params["k_tourn"],
                pc=params["pc"],
                pm_perm=params["pm_perm"],
                pm_cuts=params["pm_cuts"],
                seed=seed,
                log_convergence=True
            )
            elapsed = time.time() - start_time

            dists.append(float(best_dist))
            times.append(float(elapsed))
            histories_all.append(best_hist)
            best_inds.append(best_ind)

            print(f"    run {seed+1}/{N_RUNS} done: best_dist={best_dist:.2f}, time={elapsed:.2f}s")

        # store aggregated result row
        results.append({
            "InstanceID": inst_id,
            "Instance": inst_name,
            "ParamSet": set_name,
            "BestDist": float(np.min(dists)),
            "MeanDist": float(np.mean(dists)),
            "WorstDist": float(np.max(dists)),
            "StdDist": float(np.std(dists)),
            "BestRuntime": float(np.min(times)),
            "MeanRuntime": float(np.mean(times)),
            "WorstRuntime": float(np.max(times)),
            "RuntimeStd": float(np.std(times)),
            "Histories": histories_all,
            "BestInds": best_inds,
            "Vehicles": V,
            "Customers": N
        })

        # plots: take the run with the best distance
        best_run_idx = int(np.argmin(dists))
        out_route = os.path.join(RESULTS_DIR, f"{inst_name}_{set_name}_best_route.png")
        out_conv = os.path.join(RESULTS_DIR, f"{inst_name}_{set_name}_convergence.png")

        plot_routes_matplotlib(best_inds[best_run_idx], customers_list, depot, V,
                               title=f"{inst_name} Best Route ({set_name}) — {np.min(dists):.1f}",
                               filename=out_route)

        plot_convergence_histories(histories_all, title=f"{inst_name} Convergence ({set_name})", filename=out_conv)
        print(f"    saved plots: {out_route}, {out_conv}")

# ---------------- save results to CSV ----------------
df = pd.DataFrame(results)
# Save full results including histories (Histories column contains list-of-lists)
df.to_pickle(os.path.join(RESULTS_DIR, "results_full.pkl"))  # quick reload later
# For CSVable summary, drop the heavy lists
df_csv = df.drop(columns=["Histories", "BestInds"])
df_csv.to_csv(os.path.join(RESULTS_DIR, "results_summary.csv"), index=False)
print(f"\nSaved results_summary.csv and results_full.pkl in {RESULTS_DIR}/")

# ---------------- build solution quality----------------
tbl_quality = df.pivot_table(index="Instance", columns="ParamSet", values=["BestDist", "MeanDist", "WorstDist"])
tbl_quality.to_csv(os.path.join(RESULTS_DIR, "solution_quality.csv"))
print("\n=== Solution quality table saved ===")

# ---------------- performance plots ----------------
# Mean runtime per instance for each paramset
plot_instance_metric(df.sort_values("Instance"), metric="MeanRuntime", filename=os.path.join(RESULTS_DIR,"mean_runtime_per_instance.png"),
                     title="Mean Runtime per Instance (by ParamSet)")

# mean vs best distance plot
plt_x = np.arange(len(df))
plt.figure(figsize=(10,4))
plt.plot(plt_x, df["MeanDist"], label="MeanDist", marker='o')
plt.plot(plt_x, df["BestDist"], label="BestDist", marker='x')
plt.xticks(plt_x, df["Instance"] + " — " + df["ParamSet"], rotation=45, ha="right")
plt.ylabel("Distance")
plt.title("Mean vs Best Distance")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "mean_vs_best_distance.png"))
plt.close()

# ---------------- convergence rate (gens to within EPS) ----------------
EPS = 0.05
def gens_to_within_eps(hist, eps=EPS):
    final = hist[-1]
    thresh = final * (1 + eps)
    for g, v in enumerate(hist):
        if v <= thresh:
            return g
    return len(hist)-1

rows = []
for _, row in df.iterrows():
    histories = row["Histories"]
    gens_list = [gens_to_within_eps(h) for h in histories]
    rows.append({
        "Instance": row["Instance"],
        "ParamSet": row["ParamSet"],
        "Best": int(np.min(gens_list)),
        "Avg": float(np.mean(gens_list)),
        "Worst": int(np.max(gens_list))
    })
df_conv = pd.DataFrame(rows)
df_conv.to_csv(os.path.join(RESULTS_DIR, "convergence_rate.csv"), index=False)

print("\nAll experiments done. CSVs and plots are in the results/ folder.")
