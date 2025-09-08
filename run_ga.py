import os
import shutil
import time
import matplotlib.pyplot as plt
from matplotlib import cm

from ga.ga_solver import solve_qiea
from data.small_instances import SMALL_INSTANCE_1, SMALL_INSTANCE_2
from data.medium_instances import MEDIUM_INSTANCE_1, MEDIUM_INSTANCE_2
from data.large_instances import LARGE_INSTANCE_1, LARGE_INSTANCE_2

# ------------------- Clear previous results -------------------
if os.path.exists("results"):
    shutil.rmtree("results")
os.makedirs("results")

# ------------------- Helper Function -------------------
def plot_routes(instance, routes, save_path):
    depot_x, depot_y = instance["DEPOT"]
    plt.figure(figsize=(8, 8))
    plt.scatter(depot_x, depot_y, c='red', s=100, label="Depot")

    for cid, (x, y) in instance["CUSTOMERS"].items():
        plt.scatter(x, y, c='blue')
        plt.text(x + 0.5, y + 0.5, str(cid), fontsize=9)

    colors = cm.get_cmap('tab20').colors
    for i, route in enumerate(routes):
        x_coords = [depot_x] + [instance["CUSTOMERS"][c][0] for c in route] + [depot_x]
        y_coords = [depot_y] + [instance["CUSTOMERS"][c][1] for c in route] + [depot_y]
        plt.plot(x_coords, y_coords, color=colors[i % len(colors)], label=f"Vehicle {i+1}")

    plt.title("Vehicle Routes")
    plt.legend()
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()

# ------------------- VRP Instances -------------------
instances = {
    "Small-1": SMALL_INSTANCE_1,
    "Small-2": SMALL_INSTANCE_2,
    "Medium-1": MEDIUM_INSTANCE_1,
    "Medium-2": MEDIUM_INSTANCE_2,
    "Large-1": LARGE_INSTANCE_1,
    "Large-2": LARGE_INSTANCE_2,
}

# ------------------- QIEA Parameters -------------------
params = [
    {"pop_size": 30, "generations": 50, "delta_theta": 0.05},
    {"pop_size": 50, "generations": 100, "delta_theta": 0.05},
    {"pop_size": 80, "generations": 200, "delta_theta": 0.05},
]

n_runs = 5  # Number of independent runs per instance+param
tolerance = 1e-6  # Tolerance for float comparisons

# ------------------- Run Experiments -------------------
all_results = {}

for name, inst in instances.items():
    print(f"\n=== Processing {name} ===")
    all_results[name] = []

    for param in params:
        print(f"Running QIEA with parameters: {param}")
        run_costs = []
        run_routes = []
        run_convergences = []
        run_times = []
        run_time_to_best = []

        for run_idx in range(n_runs):
            seed = run_idx + 1
            start_time = time.time()
            best_ind, best_cost, best_routes_run, best_cost_per_gen_run = solve_qiea(
                inst,
                pop_size=param["pop_size"],
                generations=param["generations"],
                delta_theta=param["delta_theta"],
                seed=seed
            )
            run_time = time.time() - start_time
            run_times.append(run_time)
            run_costs.append(best_cost)
            run_routes.append(best_routes_run)
            run_convergences.append(best_cost_per_gen_run)

            # Find generation where best cost was first achieved
            try:
                first_best_gen = next(i for i, cost in enumerate(best_cost_per_gen_run)
                                      if abs(cost - best_cost) < tolerance)
                time_to_best = sum(run_time / len(best_cost_per_gen_run) for _ in range(first_best_gen + 1))
            except StopIteration:
                first_best_gen = 0
                time_to_best = 0.0
            run_time_to_best.append(time_to_best)

            print(f"Run {run_idx+1} | Best cost: {best_cost:.2f} found at generation {first_best_gen} (~{time_to_best:.2f}s)")

        # Aggregate results
        best_cost_overall = min(run_costs)
        avg_cost = sum(run_costs) / len(run_costs)
        worst_cost = max(run_costs)
        avg_runtime = sum(run_times) / len(run_times)
        avg_time_to_best = sum(run_time_to_best) / len(run_time_to_best)
        best_idx = run_costs.index(best_cost_overall)
        best_routes = run_routes[best_idx]
        best_convergence = run_convergences[best_idx]

        print(f"{name} | {param} | Best: {best_cost_overall:.2f}, Avg: {avg_cost:.2f}, Worst: {worst_cost:.2f}, "
              f"Avg Runtime: {avg_runtime:.2f}s, Avg Time to Best: {avg_time_to_best:.2f}s")

        # Store results
        all_results[name].append({
            "param": param,
            "best_cost": best_cost_overall,
            "avg_cost": avg_cost,
            "worst_cost": worst_cost,
            "avg_runtime": avg_runtime,
            "avg_time_to_best": avg_time_to_best,
            "best_routes": best_routes,
            "convergence": best_convergence
        })

        # ------------------- Save Plots -------------------
        # Route plot
        plot_file = f"results/{name}_routes_pop{param['pop_size']}_gen{param['generations']}.png"
        plot_routes(inst, best_routes, plot_file)
        print(f"Route plot saved to {plot_file}")

        # Convergence plot
        plt.figure()
        plt.plot(best_convergence, marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Best Cost")
        plt.title(f"{name} QIEA Convergence (pop={param['pop_size']}, gen={param['generations']})")
        plt.grid(True)
        convergence_file = f"results/{name}_convergence_pop{param['pop_size']}_gen{param['generations']}.png"
        plt.savefig(convergence_file)
        plt.close()
        print(f"Convergence plot saved to {convergence_file}")

print("\nAll experiments completed. Plots saved in 'results/' folder.")
