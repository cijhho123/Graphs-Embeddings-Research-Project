import random
import numpy as np
import matplotlib.pyplot as plt
import statistics
from collections import Counter
import networkx as nx
import os
import csv
from datetime import datetime
from collections import defaultdict


# Output directory constant
OUTPUT_DIR = "output/"

from config import getSettings
config = getSettings()

settings = config["algorithmSettings"]
graph_settings = config["graphSettings"]
alpha = settings["alpha"]

OUTPUT_DIR = "output/"

def generateRadiusValue(graph):
    t = int((int(alpha) + 1)/2)

    for vertexID in graph.graph.nodes:
        vertex = graph.graph.nodes[vertexID]['vertex']

        p = (1/graph.size)**(1/t)
        dist = []
        sum = 0.0
        for k in range(t-1):
            prob = (p**k)*(1-p)
            sum += prob
            dist.append(sum)
        dist.append(1.0)
        rand = random.random()
        for k, ceil in enumerate(dist):
            if rand < ceil:
                vertex.radius = k

def readEdge(graph, e):
    if isGreaterLabel(e.first, e.second):
        u = e.first
        v = e.second
    else:
        u = e.second
        v = e.first

    if u.label.level < u.label.baseVertex.radius:
        v.label = u.label.promote(graph)
        v.tree.append(e)
    elif u.label.base not in v.table:
        v.table.add(u.label.base)
        v.cross.append(e)

def isGreaterLabel(u, v):
    if u.label.label > v.label.label:
        return True
    elif u.label.label == v.label.label:
        return u.id > v.id
    return False

"""
    for every pair of vertices u,v - if (u,v) exist in the original graph:
        - calculate the distance of the path (u,v) in the cover graph
        - calculate the ratio origina(u,v) / cover(u,v)
""" 
def calculateStretchDistribution(original, cover):

    stretch_distribution = defaultdict(int)

    for u in original.nodes():
        for v in original.nodes():
            if u == v:
                continue
            try:
                d_orig = nx.shortest_path_length(original, source=u, target=v)
                d_cover = nx.shortest_path_length(cover, source=u, target=v)
                ratio = round(d_cover / d_orig, 5)
                stretch_distribution[ratio] += 1
            except nx.NetworkXNoPath:
                continue

    return dict(stretch_distribution)


def processStretchStatistics(data, compression_ratio, seed):
    """
    processes stretch data and saves results to output/ folder with a timestamped filename.

    Args:
        data: dictionary of ((original_distance / spanner_distance), count)

    Returns:
        A dictionary of computed statistics
    """
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate timestamped filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    plot_path = os.path.join(OUTPUT_DIR, f"{timestamp}_stretch_distribution.png")
    csv_path = os.path.join(OUTPUT_DIR, f"{timestamp}_stretch_stats.csv")

    # Create a counter of stretch values
    stretch_counter = Counter()
    total_count = 0

    for ratio, count in data.items():
        stretch_counter[ratio] += count
        total_count += count
    print(stretch_counter)
    if not stretch_counter:
        print("No valid stretch data.")
        return {}

    # Compute statistics
    all_stretches = sorted(stretch_counter.items())
    #print(all_stretches)
    avg = sum(s * c for s, c in all_stretches) / total_count
    max_stretch = max(stretch_counter.keys())

    # Median
    cumulative = 0
    median = None
    halfway = total_count / 2
    for stretch, count in all_stretches:
        cumulative += count
        if cumulative >= halfway:
            median = stretch
            break

    # Std deviation
    variance = sum(c * ((s - avg) ** 2) for s, c in all_stretches) / total_count
    std_dev = variance ** 0.5

    # Mode
    most_common = stretch_counter.most_common(1)
    mode = most_common[0][0] if most_common else None

    # Plot histogram
    plt.figure(figsize=(8, 5))
    x_vals = list(stretch_counter.keys())
    y_vals = list(stretch_counter.values())
    plt.bar(x_vals, y_vals, width=0.03, edgecolor='black')
    plt.title("Stretch Distribution Histogram")
    plt.xlabel("Stretch (spanner distance / original distance)")
    plt.ylabel("Frequency")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(plot_path)
    plt.close()

    # Save stats to CSV
    stats = {
        "compression_ratio": compression_ratio,
        "average": round(avg, 5),
        "median": round(median, 5),
        "std_dev": round(std_dev, 5),
        "mode": round(mode, 5) if isinstance(mode, float) else mode,
        "max": round(max_stretch, 5),
        "alpha": settings.get("alpha"),
        "vertex_count": graph_settings.get("vertexCount"),
        "edge_probability": graph_settings.get("edgeProbability"),
        "graph_type": graph_settings.get("graphType", {}).get("type"),
        "graph_seed": seed
    }

    with open(csv_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        for k, v in stats.items():
            writer.writerow([k, v])

    return stats


def extract_node_number(node):
    """Convert 'v1[L=1]' to 1, or return node as-is if it's already a number"""
    if isinstance(node, str) and node.startswith('v'):
        return int(node.split('[')[0][1:])  # Extract number after 'v'
    return node