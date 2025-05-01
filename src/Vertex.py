import Graph

"""
    Vertex: 
        ID - baked into the graph
        base value - integer
        level - integer
        radius - integer
        label - integer
        edge set - start with a singelton of the vertex, grows with time
"""

class Vertex:
    def __init__(self, id, base=None, radius=None, level=None, label=None, edgeSet={id}):
        self.id = id
        self.base = base
        self.radius = radius
        self.level = radius
        self.label = label
        self.edgeSet = edgeSet
