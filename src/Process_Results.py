import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Paths
AGGREGATED_CSV_PATH = "processed_output/aggregated_experiment_data.csv"
PLOTS_DIR = "processed_output/plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# Load data
df = pd.read_csv(AGGREGATED_CSV_PATH)

# Check for required columns
required_columns = {
    "compression_ratio", "average", "max", "std_dev", "mode", "median",
    "alpha", "vertex_count", "edge_probability"
}
missing = required_columns - set(df.columns)
if missing:
    print(f"Missing required columns: {missing}")
    exit()

# Descriptive axis labels
label_map = {
    "compression_ratio": "Compression Ratio",
    "average": "Stretch Average",
    "max": "Stretch Max",
    "std_dev": "Stretch Std. Dev.",
    "mode": "Stretch Mode",
    "median": "Stretch Median",
    "alpha": "Stretch Factor (α)",
    "vertex_count": "Number of Vertices (n)",
    "edge_probability": "Edge Probability (p)"
}

# Plot and save function
def save_plot(x, y, hue=None):
    print(f"Generating: {label_map[y]} vs {label_map[x]}" + (f" (hue = {label_map[hue]})" if hue else ""))

    if hue:
        plot = sns.lmplot(
            data=df, x=x, y=y, hue=hue,
            height=5, aspect=1.6,
            scatter_kws={"alpha": 0.5, "s": 30},
            line_kws={"lw": 1.5},
            ci=None, legend=True
        )
        plot.set_axis_labels(label_map[x], label_map[y])
        plot.fig.suptitle(f"{label_map[y]} vs {label_map[x]} by {label_map[hue]}", y=1.03)
        fname = f"{label_map[y]}_vs_{label_map[x]}_by_{label_map[hue]}"
    else:
        plt.figure(figsize=(8, 5))
        sns.regplot(
            data=df, x=x, y=y,
            scatter_kws={"alpha": 0.5, "s": 30},
            line_kws={"color": "red"},
            ci=None
        )
        plt.xlabel(label_map[x])
        plt.ylabel(label_map[y])
        plt.title(f"{label_map[y]} vs {label_map[x]}")
        plt.tight_layout()
        fname = f"{label_map[y]}_vs_{label_map[x]}"
        path = os.path.join(PLOTS_DIR, fname.replace(" ", "_").replace(".", "").lower() + ".png")
        plt.savefig(path)
        plt.close()
        print(f"Saved: {path}")
        return

    # Save lmplot figure
    fname = fname.replace(" ", "_").replace(".", "").lower() + ".png"
    path = os.path.join(PLOTS_DIR, fname)
    plot.savefig(path)
    plt.close()
    print(f"Saved: {path}")

# All 2D plots
relations_2d = [
    ("compression_ratio", "average"),
    ("compression_ratio", "max"),
    ("compression_ratio", "std_dev"),
    ("compression_ratio", "mode"),
    ("compression_ratio", "median"),

    ("alpha", "average"),
    ("alpha", "max"),
    ("alpha", "compression_ratio"),
    ("alpha", "std_dev"),
    ("alpha", "mode"),
    ("alpha", "median"),

    ("vertex_count", "average"),
    ("vertex_count", "compression_ratio"),
    ("vertex_count", "std_dev"),
    ("vertex_count", "max"),

    ("edge_probability", "average"),
    ("edge_probability", "compression_ratio"),
    ("edge_probability", "std_dev"),
    ("edge_probability", "max"),
]

# All 3D colored plots
relations_3d = [
    ("vertex_count", "average", "alpha"),
    ("edge_probability", "compression_ratio", "alpha"),
    ("edge_probability", "max", "vertex_count"),
    ("vertex_count", "std_dev", "alpha"),
]

# Generate all plots
for x, y in relations_2d:
    save_plot(x, y)

for x, y, hue in relations_3d:
    save_plot(x, y, hue=hue)
