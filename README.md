Vehicle Routing Problem Using Genetic Algorithm
Overview

This project implements a Genetic Algorithm (GA) to solve the Vehicle Routing Problem (VRP), finding efficient routes for multiple vehicles to serve all customers from a central depot.

Project Structure
VRP_GA/
├── data/          # VRP instances (small, medium, large)
├── ga/            # GA implementation
├── run_ga.py      # Main script
├── requirements.txt
├── README.md
└── .gitignore
git
Installation
git clone <repo-url>
cd VRP_GA
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

Usage
python run_ga.py


Generates route and convergence plots (in results/).

GA parameters are configurable inside run_ga.py.

GA Design

Chromosome: customer permutation

Selection: Tournament selection

Crossover: Ordered Crossover

Mutation: Swap mutation

Fitness: Total Euclidean distance of all routes

Notes

results/ is ignored in Git.

VRP instances: small, medium, large.

Outputs best, average, and worst costs for each instance.