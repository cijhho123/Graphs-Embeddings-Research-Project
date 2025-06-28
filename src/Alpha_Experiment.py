import json
import subprocess
import time
import os

# Paths
CONFIG_PATH = "src/config.json"
MAIN_SCRIPT = "src/Main.py"

# Parameters
setup_multiplier = 5
vertex_count = 200
edge_probability = 0.15
alphas = list(range(1, 50, 2))  # 1, 3, 5, ..., 49

def run_experiment(alpha, run_number):
    print(f"[α={alpha}] Run {run_number+1}/{setup_multiplier}")

    # Write config to src/config.json
    config = {
        "softwareSettings": {
            "debug": True
        },
        "graphSettings": {
            "graphType": {
                "type": "unweighted",
                "weight": 1
            },
            "vertexCount": vertex_count,
            "edgeProbability": edge_probability,
            "graphSeed": None  # Random seed
        },
        "algorithmSettings": {
            "alpha": alpha
        }
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    # Run Main.py normally
    subprocess.run(["python", MAIN_SCRIPT], check=True)
    time.sleep(1)

if __name__ == "__main__":
    for alpha in alphas:
        for run in range(setup_multiplier):
            try:
                run_experiment(alpha, run)
            except subprocess.CalledProcessError as e:
                print(f"Experiment failed: {e}")
