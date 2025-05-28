import random
import numpy as np

from config import getSettings
config = getSettings()

settings = config["algorithmSettings"]
alpha = settings["alpha"]

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
        if e.first > e.second:  # need to add comparison by label and then by index
            u = e.first
            v = e.second
        else:
            u = e.second
            v= e.first
        if u.label.level < u.labe.baseVertex.radius:
            v.label.label = u.label.label + graph.size
            v.tree.append(e)
        elif u.label.base not in v.table:
            v.table.append(u.label.base) 
            v.cross.append(e)