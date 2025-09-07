import os
import shutil
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

# QIEA parameter sets (match solve_qiea signature)
params = [
    {"pop_size": 30, "generations": 50, "delta_theta": 0.05},
    {"pop_size": 50, "generations": 100, "delta_theta": 0.05},
    {"pop_size": 80, "generations": 200, "delta_theta": 0.05},
]

n_runs = 5  # Independent runs per instance+param

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

        for run_idx in range(n_runs):
            seed = run_idx + 1  # reproducible runs
            best_ind, best_cost, best_routes, best_cost_per_gen = solve_qiea(
                inst,
                pop_size=param["pop_size"],
                generations=param["generations"],
                delta_theta=param["delta_theta"],
                seed=seed
            )
            run_costs.append(best_cost)
            run_routes.append(best_routes)
            run_convergences.append(best_cost_per_gen)

        # Aggregate results
        best_cost = min(run_costs)
        avg_cost = sum(run_costs) / len(run_costs)
        worst_cost = max(run_costs)
        best_idx = run_costs.index(best_cost)
        best_routes = run_routes[best_idx]
        best_convergence = run_convergences[best_idx]

        print(f"{name} | {param} | Best: {best_cost:.2f}, Avg: {avg_cost:.2f}, Worst: {worst_cost:.2f}")

        # Store results
        all_results[name].append({
            "param": param,
            "best_cost": best_cost,
            "avg_cost": avg_cost,
            "worst_cost": worst_cost,
            "best_routes": best_routes,
            "convergence": best_convergence
        })

    
        best_ind_plot, best_cost_plot, best_routes_plot, best_convergence_plot = solve_qiea(
            inst,
            pop_size=param["pop_size"],
            generations=param["generations"],
            delta_theta=param["delta_theta"],
            seed=1  # fixed seed for reproducible plots
        )

        # Route plot
        plot_file = f"results/{name}_routes_pop{param['pop_size']}_gen{param['generations']}.png"
        plot_routes(inst, best_routes_plot, plot_file)
        print(f"Route plot saved to {plot_file}")

        # Convergence plot
        plt.figure()
        plt.plot(best_convergence_plot, marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Best Cost")
        plt.title(f"{name} QIEA Convergence (pop={param['pop_size']}, gen={param['generations']})")
        plt.grid(True)
        convergence_file = f"results/{name}_convergence_pop{param['pop_size']}_gen{param['generations']}.png"
        plt.savefig(convergence_file)
        plt.close()
        print(f"Convergence plot saved to {convergence_file}")

print("\nAll experiments completed. Plots saved in 'results/' folder.")
