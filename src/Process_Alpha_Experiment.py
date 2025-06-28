import os
import pandas as pd
import matplotlib.pyplot as plt

ALPHA_OUTPUT_DIR = "alpha_output"
PROCESSED_OUTPUT_DIR = "processed_output"
AGGREGATED_CSV_PATH = os.path.join(PROCESSED_OUTPUT_DIR, "alpha_experiment_aggregated.csv")
PLOT_PATH = os.path.join(PROCESSED_OUTPUT_DIR, "alpha_experiment_graph.png")

all_data = []

print("Looking for CSVs in:", ALPHA_OUTPUT_DIR)

files = [f for f in os.listdir(ALPHA_OUTPUT_DIR) if f.endswith("_stretch_stats.csv")]
print(f"Found {len(files)} CSV files.")

for file in files:
    path = os.path.join(ALPHA_OUTPUT_DIR, file)
    try:
        df = pd.read_csv(path)
        if set(df.columns) != {"Metric", "Value"}:
            print(f"Skipping malformed file: {file}")
            continue

        # Convert to dict format (Metric: Value)
        flat = df.set_index("Metric")["Value"].to_dict()

        # Cast numeric fields
        for key in ["alpha", "average", "max", "std_dev", "compression_ratio"]:
            if key in flat:
                try:
                    flat[key] = float(flat[key])
                except:
                    print(f"Skipping non-numeric value in {file}: {key}={flat[key]}")
                    flat = None
                    break

        if flat:
            all_data.append(flat)

    except Exception as e:
        print(f"Failed to process {file}: {e}")

if not all_data:
    print("No valid data found.")
    exit()

df = pd.DataFrame(all_data)
df = df.dropna(subset=["alpha", "average", "std_dev", "compression_ratio"])
df["alpha"] = df["alpha"].astype(int)

# Group by alpha, compute mean
agg = df.groupby("alpha").agg({
    "average": "mean",
    "max": "mean",
    "std_dev": "mean",
    "compression_ratio": "mean"
}).reset_index()

# Save aggregated CSV
agg.to_csv(AGGREGATED_CSV_PATH, index=False)
print(f"Saved aggregated data to {AGGREGATED_CSV_PATH}")

# Plot
plt.figure(figsize=(10, 6))
plt.plot(agg["alpha"], agg["average"], marker="o", label="Average Stretch")

# Annotate each point with (x, y)
for x, y in zip(agg["alpha"], agg["average"]):
    plt.text(x, y + 0.01, f"({x}, {y:.2f})", ha='center', fontsize=8, color='darkblue')

plt.xlabel("Stretch Factor α")
plt.ylabel("Average Stretch")
plt.title("Stretch Average vs. α (Alpha Experiment)")
plt.grid(True)
plt.tight_layout()
plt.savefig(PLOT_PATH)
print(f"Saved plot to {PLOT_PATH}")
