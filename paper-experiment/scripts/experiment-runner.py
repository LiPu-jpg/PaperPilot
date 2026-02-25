"""
Experiment Runner

Execute experiments with grid search, random search, or single run.
"""

import argparse
import json
import subprocess
import itertools
from pathlib import Path
from typing import Dict, List, Any


def run_experiment(config: Dict[str, Any], log_dir: str) -> Dict:
    """Run a single experiment with given config."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Build command
    cmd = ["python", "train.py"]
    for key, value in config.items():
        cmd.extend([f"--{key}", str(value)])

    # Run and capture output
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=log_path.parent)

    return {
        "config": config,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }


def grid_search(configs: List[Dict], log_dir: str) -> List[Dict]:
    """Run grid search over configs."""
    results = []
    for i, config in enumerate(configs):
        print(f"Running experiment {i + 1}/{len(configs)}: {config}")
        result = run_experiment(config, f"{log_dir}/exp_{i}")
        results.append(result)
    return results


def random_search(config_space: Dict, num_trials: int, log_dir: str) -> List[Dict]:
    """Run random search over config space."""
    import random

    results = []
    for i in range(num_trials):
        config = {k: random.choice(v) for k, v in config_space.items()}
        print(f"Running trial {i + 1}/{num_trials}: {config}")
        result = run_experiment(config, f"{log_dir}/trial_{i}")
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description="Run experiments")
    parser.add_argument("--config", "-c", help="Single config JSON file")
    parser.add_argument("--grid", "-g", help="Grid search configs JSON")
    parser.add_argument("--random", "-r", help="Random search config space JSON")
    parser.add_argument(
        "--trials", "-n", type=int, default=10, help="Number of random search trials"
    )
    parser.add_argument(
        "--log-dir", "-l", default="logs/experiments", help="Log directory"
    )
    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            config = json.load(f)
        results = [run_experiment(config, args.log_dir)]
    elif args.grid:
        with open(args.grid) as f:
            configs = json.load(f)
        results = grid_search(configs, args.log_dir)
    elif args.random:
        with open(args.random) as f:
            config_space = json.load(f)
        results = random_search(config_space, args.trials, args.log_dir)
    else:
        print("Please specify --config, --grid, or --random")
        return

    # Save results
    with open(f"{args.log_dir}/results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {args.log_dir}/results.json")


if __name__ == "__main__":
    main()
