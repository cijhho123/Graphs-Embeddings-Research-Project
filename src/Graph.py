import networkx as nx # https://www.rustworkx.org/networkx.html#
import random

from config import getSettings
config = getSettings()
settings = config["graphSettings"]

"""
    A class for a weighted undirected Graph G = (V, E)

    vertex should include unique identifier(i), radius(r), label(p = i), base value(b),
    edge set (sp) divided into tree edges(t) and cross edges(x), table(m)
    class labels includes base vertex(w), level(l), b(b), radius(r) 
    edges have labels.
"""

class Graph:
    def __init__(self):
        self.size = settings["vertexCount"]             # Number of vertices (size)
        self.edgeProb = settings["edgeProbability"]     # Probability for edge creation
        self.graphType = settings["graphType"]          # Graph type (weighted or unweighted)
        self.seed = settings["graphSeed"]               # Seed for random number generation (optional)

    def generateRandomGraph(self):
        # Generate a stochasic random graph
        graph =  nx.erdos_renyi_graph(self.n, self.p, self.seed) 
        
        # Get graph type (weighted / unweighted)
        lower = -1, upper = -1
        if (self.graphType["type"] == "weighted"):
            lower = self.graphType["lowerBoundWeight"]
            upper = self.graphType["upperBoundWeight"]
        elif (self.graphType["type"] == "unweighted"):
            lower = upper = self.graphType["weight"]
        
        # Generate edges weight
        for u, v in graph.edges():
            graph[u][v] = random.randint(lower, upper)

        self.graph = graph
    
    def generateEmptyGraph(self):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.n))
