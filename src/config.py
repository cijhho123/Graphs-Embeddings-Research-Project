import json
import os

weightedGraphType =  {
    "type": "weighted",
    "lowerBoundWeight": 1,
    "upperBoundWeight": 10
}

unweightedGraphType = {
    "type": "unweighted",
    "weight": 1
}

defaultConfig = {   
    "softwareSettings": {
        "debug": True
    },

    "graphSettings": {
        "graphType": weightedGraphType,     # weighted vs unweighted graph
        "vertexCount": 100,                 # Graph size |V| = vertexCount
        "edgeProbability": 0.3,             # The probability of each edge to exist, each edge is an i.i.d. random varible
        "graphSeed": None                   # Seed to generate the random graph, None for random seed
    },
    
    "algorithmSettings": {
        "alpha": 5  # For a parameter α, α ≥ 1, a subgraph G' of the graph G = (V, E) is called an α-spanner
                    # of G if for every pair of vertices x, y ∈ V , dist_G'(x, y) ≤ α · dist_G(x, y)
    }
}




def getSettings():
    try:
        with open("config.json", "r") as f:
            print("Using existing config file.")
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("Couldn't find a config file, using default values.")
        return defaultConfig