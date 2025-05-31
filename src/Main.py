from Graph import Graph, printGraph
from Edge import Edge
from Spanner import readEdge, generateRadiusValue
import networkx as nx
from Label import Label

from config import getSettings
config = getSettings()

def main():
    graph = initRandomGraph()
    cover = getSpanner(graph)
    printGraph(cover)


def initRandomGraph():
    graph =  Graph()
    graph.generateRandomGraph()
    graph.initVertices()
    return graph

def initEmptyGraph():
    emptyGraph = Graph()
    emptyGraph.generateEmptyGraph()
    return emptyGraph

def getSpanner(graph):
    generateRadiusValue(graph)
    for vertexID in graph.graph.nodes:
        vertex = graph.graph.nodes[vertexID]['vertex']
        vertex.label = Label(graph, vertex)  # base = vertex.id, level = 0
    
    for u, v in graph.edges():
        e = Edge(graph.graph.nodes[u]['vertex'], graph.graph.nodes[v]['vertex'])
        readEdge(graph, e)
    
    spanner = nx.Graph()
    for v in graph.vertices():
        for e in v.tree:
            spanner.add_edge(e.first, e.second)
        for e in v.cross:
            spanner.add_edge(e.first, e.second)

    return spanner


if __name__ == "__main__":
    main()