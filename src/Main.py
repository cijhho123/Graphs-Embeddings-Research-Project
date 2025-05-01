from Graph import Graph, readEdge, createGraph

from config import getSettings
config = getSettings()

def main():
    graph = initRandomGraph()

    cover = getSpanner(graph)


def initRandomGraph():
    graph =  Graph()
    graph.generateRandomGraph()
    return graph

def initEmptyGraph():
    emptyGraph = Graph()
    emptyGraph.generateEmptyGraph()
    return emptyGraph

def getSpanner(graph):
    graph.assignradii(config["algorithmSettings"]['alpha']) # TODO need to change it, the func moved to Spanner.py
    cover = initEmptyGraph()
    for e in graph.edges:
        readEdge(e)
    for v in graph.vertices:
        cover.append(v.t)  # should be changed to add_edges when function exists
        cover.append(v.x)  # should be changed to add_edges when function exists

    return cover


if __name__ == "__main__":
    main()