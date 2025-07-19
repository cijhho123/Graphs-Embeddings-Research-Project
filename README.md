# Streaming Sparse Spanner Construction

An implementation and further analysis of the paper:  
**"Streaming and Fully Dynamic Centralized Algorithms for Constructing and Maintaining Sparse Spanners"** by Michael Elkin (2011)

## Overview

This project implements Elkin's streaming algorithm for building sparse spanners of unweighted graphs.  
Graph spanners are subgraphs that preserve approximate shortest paths. The goal is to construct a sparse subgraph where for every original edge (u, v), the distance in the spanner is at most (2t−1).

The algorithm is notable for:
- **O(1) time per edge in streaming**
- **Efficient memory usage**
- **Provably small spanner size with strong stretch guarantees**
- **Support for dynamic (insertion/deletion) edge updates**

The research paper and full report are available under **/Administrative/** folder.

## Project Structure

```
src/
├── Aggregate_Results.py         # Combines all CSV results from experiments
├── Alpha_Experiment.py          # Script for running a focused alpha-varying experiment
├── config.py / config.json      # Configuration files for all runs
├── Edge.py                      # Basic edge representation
├── Experiments.py               # Main experimental runner
├── Graph.py                     # Generates and holds the graph structure
├── Label.py                     # Manages label promotion and encoding
├── Main.py                      # Entry point for graph generation and spanner construction
├── Process_Alpha_Experiment.py  # Post-processes alpha experiment results
├── Process_Results.py           # Plots and analyzes aggregated experiment results
├── Spanner.py                   # Core algorithm logic
├── Vertex.py                    # Represents vertex logic and local state
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/cijhho123/Embeddings-of-Graphs-Project
cd Embeddings-of-Graphs-Project
```
Alternatively, unzip the provided project archive.

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate         # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Experiments

Run the full set of baseline experiments:

```bash
python src/Experiments.py
```

Results will be saved to the `output/` directory.

### 5. Aggregate and Analyze Results

```bash
python src/Aggregate_Results.py
python src/Process_Results.py
```

This will generate CSV summaries and graphs under `processed_output/`.

---

## Research Goals

This project studies the behavior of the streaming spanner algorithm under different graph configurations:

- Number of vertices `n`
- Edge probability `p` (density)
- Stretch factor `α` (tightness of paths)

We examine:
- Compression ratio: size of the spanner vs. original graph
- Stretch statistics: average, std dev, max, etc.
- Tradeoffs between stretch and sparsity

### Research Questions

- How does average stretch evolve with increasing α?
- When is the compression ratio maximized?
- How do n and p impact stretch and spanner size?
- Are there diminishing returns at high α?

---

## Key Findings

- **Average Stretch vs. α**: Slight increase as α grows; the gain plateaus.
- **Compression Ratio vs. α**: Improves with α until ~25–35, then stabilizes or worsens.
- **Edge Probability p**: Denser graphs allow more compression, but can slightly increase average stretch.
- **Vertex Count n**: Larger graphs exhibit higher compressibility.

### Alpha Experiment

To further analyze α’s role, we ran a focused experiment varying only α while fixing n and p. The results confirmed:
- Compression improves with α up to the point where t >= log (n).
- Beyond that, further increases in α show diminishing compression benefits.

---

## Output Format

Each experiment generates:
- A CSV summary of stretch and compression statistics
- A histogram PNG showing stretch value distribution

**Example CSV Output:**
```
Metric,Value
compression_ratio,11.23
average,1.65
std_dev,0.53
max,4.0
alpha,15
vertex_count,200
edge_probability,0.3
```

---

## Conclusion

Elkin’s streaming spanner algorithm offers strong theoretical guarantees and shows promising empirical performance.  
It consistently achieves low average stretch even in compressed graphs and adapts well across densities and sizes.  
Future work could extend the approach to weighted graphs and evaluate it on real-world datasets.

---

## License

This project is intended for educational and research purposes only.

## Credits

Special thanks to **Prof. Michael Elkin** for his foundational work and guidance, which directly inspired this project.
