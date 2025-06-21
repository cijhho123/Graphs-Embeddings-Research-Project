import networkx as nx # https://networkx.org/documentation/stable/tutorial.html
import random

from Vertex import Vertex
from Label import Label

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
        
        if settings["graphSeed"] is None:
            self.seed = random.randint(0, 10**6)        # Generate random seed
        else:
            self.seed = settings["graphSeed"]           # Use seed from config file

    def generateRandomGraph(self):
        # Generate a stochasic random graph
        self.graph = nx.erdos_renyi_graph(self.size, self.edgeProb, self.seed)

        while not nx.is_connected(self.graph):
            self.seed = random.randint(0, 10**6)
            self.graph = nx.erdos_renyi_graph(self.size, self.edgeProb, self.seed)

        # Get graph type (weighted / unweighted)
        lower = upper = -1
        if (self.graphType["type"] == "weighted"):
            lower = self.graphType["lowerBoundWeight"]
            upper = self.graphType["upperBoundWeight"]
        elif (self.graphType["type"] == "unweighted"):
            lower = upper = self.graphType["weight"]
        lower = int(lower)
        upper = int(upper)

        # Generate edges weight
        for u, v in self.graph.edges():
            self.graph[u][v]['weight'] = random.randint(lower, upper)

    
    def generateEmptyGraph(self):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(self.n))

    def initVertices(self):
        for x in range (0, self.size):
            self.graph.nodes[x]['vertex'] = Vertex(x)

    def edges(self):
        return self.graph.edges()
    
    def vertices(self):
        return [self.graph.nodes[i]['vertex'] for i in self.graph.nodes]

def printGraph(graph):
    print("Graph edges:")
    for u, v in graph.edges():
        print(f"{u} --- {v}")