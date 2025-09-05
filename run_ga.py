import os
import matplotlib.pyplot as plt
from matplotlib import cm
from ga.ga_solver import solve_ga
from data.small_instances import SMALL_INSTANCE_1, SMALL_INSTANCE_2
from data.medium_instances import MEDIUM_INSTANCE_1, MEDIUM_INSTANCE_2
from data.large_instances import LARGE_INSTANCE_1, LARGE_INSTANCE_2

# ------------------- Setup -------------------
# Ensure 'results/' folder exists
if not os.path.exists("results"):
    os.makedirs("results")

# Define all VRP instances
instances = {
    "Small-1": SMALL_INSTANCE_1,
    "Small-2": SMALL_INSTANCE_2,
    "Medium-1": MEDIUM_INSTANCE_1,
    "Medium-2": MEDIUM_INSTANCE_2,
    "Large-1": LARGE_INSTANCE_1,
    "Large-2": LARGE_INSTANCE_2,
}

# GA parameter sets to test
params = [
    {"pop_size": 30, "generations": 50, "pc": 0.8, "pm": 0.1},
    {"pop_size": 50, "generations": 100, "pc": 0.9, "pm": 0.2},
    {"pop_size": 80, "generations": 200, "pc": 0.7, "pm": 0.05},
]

# Number of independent runs per instance+parameter set
n_runs = 5

# ------------------- Helper Function -------------------
def plot_routes(instance, routes, save_path):
    """Plot depot, customers, and vehicle routes with distinct colors."""
    depot_x, depot_y = instance["DEPOT"]
    plt.figure(figsize=(8, 8))

    # Depot
    plt.scatter(depot_x, depot_y, c='red', s=100, label="Depot")

    # Customers
    for cid, (x, y) in instance["CUSTOMERS"].items():
        plt.scatter(x, y, c='blue')
        plt.text(x + 0.5, y + 0.5, str(cid), fontsize=9)

    # Vehicle routes
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

# ------------------- Run Experiments -------------------
all_results = {}

for name, inst in instances.items():
    print(f"\n=== Processing {name} ===")
    all_results[name] = []

    for param in params:
        print(f"Running GA with parameters: {param}")
        run_costs = []
        run_routes = []
        run_convergences = []

        # Multiple independent runs for reliability
        for run_idx in range(n_runs):
            # Optional seed ensures reproducibility
            seed = run_idx + 1
            best_ind, best_cost, best_routes, best_cost_per_gen = solve_ga(inst, **param, seed=seed)
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

        # Store for plotting summary
        all_results[name].append({
            "param": param,
            "best_cost": best_cost,
            "avg_cost": avg_cost,
            "worst_cost": worst_cost,
            "best_routes": best_routes,
            "convergence": best_convergence
        })

        # Save route plot
        plot_file = f"results/{name}_routes_pop{param['pop_size']}_gen{param['generations']}.png"
        plot_routes(inst, best_routes, plot_file)
        print(f"Route plot saved to {plot_file}")

        # Save convergence plot
        plt.figure()
        plt.plot(best_convergence, marker='o')
        plt.xlabel("Generation")
        plt.ylabel("Best Cost")
        plt.title(f"{name} GA Convergence (pop={param['pop_size']}, gen={param['generations']})")
        plt.grid(True)
        convergence_file = f"results/{name}_convergence_pop{param['pop_size']}_gen{param['generations']}.png"
        plt.savefig(convergence_file)
        plt.close()
        print(f"Convergence plot saved to {convergence_file}")

#Best cost vs population size plots
for name, results in all_results.items():
    pop_sizes = [r["param"]["pop_size"] for r in results]
    best_costs = [r["best_cost"] for r in results]

    plt.figure()
    plt.plot(pop_sizes, best_costs, marker='o', linestyle='-', color='blue')
    plt.xlabel("Population Size")
    plt.ylabel("Best Cost")
    plt.title(f"{name}: Best Cost vs Population Size")
    plt.grid(True)
    plot_filename = f"results/{name}_best_cost_vs_pop.png"
    plt.savefig(plot_filename)
    plt.close()
    print(f"Best cost vs population plot saved to {plot_filename}")

print("\nAll experiments completed. Plots saved in 'results/' folder.")
