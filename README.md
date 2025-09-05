# Vehicle Routing Problem Using Genetic Algorithm

## Overview

This project implements a Genetic Algorithm (GA) to solve the Vehicle Routing Problem (VRP). The GA finds efficient routes for multiple vehicles to serve all customers from a central depot while minimizing the total travel distance.

## Installation

Clone the repository, create a virtual environment, and install dependencies:

```bash
git clone <repo-url>
cd VRP_GA
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Usage

Run the main script to execute the GA on all provided VRP instances:

```bash
python run_ga.py
```

This generates:

* Route plots showing the best vehicle routes
* Convergence plots showing best cost per generation

Both types of plots are saved in the `results/` folder. GA parameters (population size, generations, crossover probability, mutation probability) can be configured inside `run_ga.py`.

## GA Design

* **Chromosome Representation:** Each individual is a permutation of customer indices
* **Selection:** Tournament selection
* **Crossover:** Ordered Crossover (OX)
* **Mutation:** Swap mutation
* **Fitness Function:** Total Euclidean distance of all vehicle routes (lower is better)

## VRP Instances

The project includes VRP datasets of different sizes:

* **Small:** 2–3 vehicles, 10–12 customers
* **Medium:** 15–22 vehicles, 16–20 customers
* **Large:** 45–50 vehicles, 50 customers

## Outputs

For each instance and GA parameter set, the script outputs:

* Best, average, and worst cost (total route distance)
* Vehicle route plots
* GA convergence plots

## Notes

* The `results/` folder is ignored in Git
* The GA is configurable and can be tested on custom VRP instances
* Code is written in Python and requires `numpy`, `matplotlib`, `pandas`, `networkx`, and `tqdm`

## Example

For example, running the Small-1 instance with default GA parameters may produce:

* Best cost: 219.57
* Average cost: 232.70
* Worst cost
