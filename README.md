# Vehicle Routing Problem Solver using Genetic Algorithms

## Overview
This project implements a genetic algorithm-based solver for the Vehicle Routing Problem (VRP). The solver optimizes delivery routes for multiple vehicles serving customers from a central depot, aiming to minimize total travel distance while respecting vehicle constraints.

## Features

### Genetic Algorithm Core
- **Advanced Chromosome Design**
  - Dual-part encoding (permutation + cuts)
  - Efficient route representation
  - Vehicle assignment optimization

- **Sophisticated Genetic Operators**
  - Order Crossover (OX) for route permutations
  - Custom cuts crossover for vehicle assignments
  - Adaptive mutation rates
  - Route-aware mutation strategies

### Comprehensive Analysis Tools
- Route visualization with matplotlib
- Convergence history tracking
- Performance metrics collection
- Solution quality analysis

### Configurable Parameters
Three pre-tuned parameter sets:
```python
"Standard": {
    "pop_size": 80,
    "generations": 300,
    "k_tourn": 3,
    "pc": 0.8,
    "pm_perm": 0.02,
    "pm_cuts": 0.08
}

"Large_Scale": {
    "pop_size": 150,
    "generations": 500,
    "k_tourn": 3,
    "pc": 0.85,
    "pm_perm": 0.05,
    "pm_cuts": 0.15
}

"Compact": {
    "pop_size": 30,
    "generations": 200,
    "k_tourn": 5,
    "pc": 0.7,
    "pm_perm": 0.008,
    "pm_cuts": 0.3
}
```

## Requirements

```bash
numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.4.0
seaborn>=0.11.0
```

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VRP_GA.git
cd VRP_GA
```

2. Set up environment and install:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Run the solver:
```bash
python run_ga.py
```

## Project Structure

```
VRP_GA/
├── ga/                     # Genetic Algorithm core
│   ├── chromosome.py      # Chromosome representation
│   ├── fitness.py         # Fitness calculations
│   ├── ga_solver.py       # Main GA implementation
│   └── operators.py       # Genetic operators
├── data/                  # Problem instances
│   ├── small_instances.py
│   ├── medium_instances.py
│   └── large_instances.py
├── utils.py              # Utility functions
├── plots_tables.py       # Visualization tools
└── run_ga.py            # Main execution script
```

## Output

The solver generates comprehensive results in the `results/` directory:

- `results_summary.csv`: Summary statistics for all runs
- `solution_quality.csv`: Detailed solution quality metrics
- `*_best_route.png`: Visualizations of best routes found
- `*_convergence.png`: Convergence plots
- Performance analysis plots

## Example Output

```
=== Instance Small-1: N=12, V=2 ===
  ParamSet: Standard -> {...}
    run 1/15 done: best_dist=245.32, time=1.23s
    saved plots: results/Small-1_Standard_best_route.png, 
                results/Small-1_Standard_convergence.png
```

## Analysis Features

- Route distance optimization
- Convergence rate analysis
- Runtime performance metrics
- Solution quality comparisons
- Visual route representations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.


## Future Improvements

- [ ] Multi-objective optimization support
- [ ] Additional genetic operators
- [ ] Parallel computation capabilities
- [ ] Real-time visualization
- [ ] API integration capabilities
