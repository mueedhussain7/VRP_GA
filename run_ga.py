import os, shutil, time, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Define consistent colors for each parameter set
colors = {'Standard': '#1f77b4', 'Large_Scale': '#2ca02c', 'compact': '#ff7f0e'}

# 1. Solution Quality Bar Chart
fig, ax = plt.subplots(figsize=(12, 6))
instances_ordered = ['Small-1', 'Small-2', 'Medium-1', 'Medium-2', 'Large-1', 'Large-2']
x = np.arange(len(instances_ordered))
width = 0.25

for i, param_set in enumerate(['Standard', 'Large_Scale', 'compact']):
    data = df[df['ParamSet'] == param_set]
    distances = [data[data['Instance'] == inst]['MeanDist'].values[0] for inst in instances_ordered]
    std_devs = [data[data['Instance'] == inst]['StdDist'].values[0] for inst in instances_ordered]
    
    bars = ax.bar(x + i*width - width, distances, width, 
                   label=param_set, color=colors[param_set], alpha=0.8,
                   yerr=std_devs, capsize=3, ecolor='gray')

ax.set_xlabel('Instance', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Distance', fontsize=12, fontweight='bold')
ax.set_title('Solution Quality Comparison Across All Instances', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(instances_ordered, rotation=0)
ax.legend(title='Configuration', framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'solution_quality_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

# 2. Runtime Comparison (Log Scale)
fig, ax = plt.subplots(figsize=(12, 6))
for i, param_set in enumerate(['Standard', 'Large_Scale', 'compact']):
    data = df[df['ParamSet'] == param_set]
    runtimes = [data[data['Instance'] == inst]['MeanRuntime'].values[0] for inst in instances_ordered]
    bars = ax.bar(x + i*width - width, runtimes, width, 
                   label=param_set, color=colors[param_set], alpha=0.8)

ax.set_xlabel('Instance', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Runtime (seconds, log scale)', fontsize=12, fontweight='bold')
ax.set_title('Runtime Performance Comparison', fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(instances_ordered, rotation=0)
ax.set_yscale('log')
ax.legend(title='Configuration', framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y', which='both')
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'runtime_comparison.png'), dpi=300, bbox_inches='tight')
plt.close()

# 3. Convergence Rate Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
heatmap_data = df_conv.pivot(index='Instance', columns='ParamSet', values='Avg')
heatmap_data = heatmap_data[['Standard', 'Large_Scale', 'compact']]
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd_r', 
            cbar_kws={'label': 'Generations to Convergence'},
            vmin=0, vmax=300)
ax.set_xlabel('Configuration', fontsize=12, fontweight='bold')
ax.set_ylabel('Instance', fontsize=12, fontweight='bold')
ax.set_title('Average Generations to Reach 95% of Final Solution', fontsize=13, fontweight='bold')
plt.setp(ax.get_xticklabels(), rotation=0, ha='center')
plt.setp(ax.get_yticklabels(), rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, 'convergence_heatmap.png'), dpi=300, bbox_inches='tight')
plt.close()

print("\nAll experiments done. CSVs and plots are in the results/ folder.")
