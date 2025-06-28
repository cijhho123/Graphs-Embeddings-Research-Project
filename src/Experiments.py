import json
import subprocess
import time
import os
from itertools import product

CONFIG_PATH = "src/config.json"
MAIN_SCRIPT = "src/Main.py"

# Parameters to test
setup_multiplier = 3       # how many experiments do with each setup (specific combination of parameters)
vertex_counts = [5, 20, 50, 100, 150, 200, 250, 300]   # over 300 it takes too much time per experimet
edge_probabilities = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
alphas = [1, 3, 5, 7, 15, 25, 35, 49]  # stretch factor

def run_experiment(n, p, alpha, counter):
    print(f"Running experiment: n={n}, p={p}, alpha={alpha} for the {counter+1}th time")

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    config["graphSettings"]["vertexCount"] = n
    config["graphSettings"]["edgeProbability"] = p
    config["graphSettings"]["graphSeed"] = None  # Ensures randomness
    config["algorithmSettings"]["alpha"] = alpha

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

    subprocess.run(["python", MAIN_SCRIPT], check=True)
    time.sleep(1)  #  delay between runs

if __name__ == "__main__":
    for i in range(setup_multiplier):
        for n, p, alpha in product(vertex_counts, edge_probabilities, alphas):
            try:
                run_experiment(n, p, alpha, i)
            except subprocess.CalledProcessError as e:
                print(f"Experiment failed: {e}")
