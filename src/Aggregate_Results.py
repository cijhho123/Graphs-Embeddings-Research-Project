import os
import pandas as pd

OUTPUT_DIR = "output"
PROCESSED_OUTPUT = "processed_output"
os.makedirs(PROCESSED_OUTPUT, exist_ok=True)

csv_files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".csv")]

all_data = []
for csv_file in csv_files:
    path = os.path.join(OUTPUT_DIR, csv_file)
    try:
        df = pd.read_csv(path)
        df = df.set_index("Metric").T  # convert vertical metrics to horizontal row
        df["source_file"] = csv_file
        all_data.append(df)
    except Exception as e:
        print(f"Skipping {csv_file} due to error: {e}")

if not all_data:
    print("No valid CSVs found.")
else:
    aggregated = pd.concat(all_data, ignore_index=True)
    save_path = os.path.join(PROCESSED_OUTPUT, "aggregated_experiment_data.csv")
    aggregated.to_csv(save_path, index=False)
    print(f"Aggregated CSV saved to: {save_path}")
