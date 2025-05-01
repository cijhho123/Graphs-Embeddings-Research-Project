import random

from config import getSettings
config = getSettings()

settings = config["algorithmSettings"]
alpha = settings["alpha"]

def assignRadii(graph, t):
    for v in graph.vertices:
        p = (1/graph.n)**(1/graph.n)
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
                v.radius = k
                

def readEdge(graph, e):
        if e.first > e.second:  # need to add comparison by label and then by index
            u = e.first
            v = e.second
        else:
            u = e.second
            v= e.first

        if u.p in v.m:  # really not sure about this line and what selected means 
            v.p = u.p + graph.n
            v.t.append(e)
        elif u.p.b not in v.m:
            v.m.append(u.p.b)
            v.x.append(e)