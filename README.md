# Vehicle Routing Problem Using Quantum-Inspired Evolutionary Algorithm (QIEA)

## Overview

This project implements a Quantum-Inspired Evolutionary Algorithm (QIEA) to solve the Vehicle Routing Problem (VRP). The QIEA finds efficient routes for multiple vehicles to serve all customers from a central depot while minimizing the total travel distance.

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

Run the main script to execute QIEA on all provided VRP instances:

```bash
python run_ga.py
```

This generates:

* Route plots showing the best vehicle routes
* Convergence plots showing best cost per generation

Both types of plots are saved in the `results/` folder. QIEA parameters (`pop_size`, `generations`, `delta_theta`) can be configured inside `run_ga.py`.

## QIEA Design

* Chromosome Representation: Each individual is a permutation of customer indices
* Selection: Tournament selection
* Quantum-inspired update: Rotation of probability amplitudes towards the best solution
* Fitness Function: Total Euclidean distance of all vehicle routes (lower is better)

## VRP Instances

* **Small:** 2–3 vehicles, 10–12 customers
* **Medium:** 15–22 vehicles, 16–20 customers
* **Large:** 45–50 vehicles, 50 customers

## Outputs

For each instance and parameter set, the script outputs:

* Best, average, and worst cost (total route distance)
* Vehicle route plots
* QIEA convergence plots
