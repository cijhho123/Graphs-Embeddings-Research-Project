from Label import Label 
"""
    Vertex: 
        ID - baked into the graph
        label - integer (p starts as id)
        radius - integer
        edge set - start with a singelton of the vertex, grows with time (Sp(v))

        tree edges - subset of edge set (T(v))
        cross edges - subset of edge set (X(v))
        table - initially empty, stores all base values of level P. (M(v))

"""

class Vertex:
    def __init__(self, id):
        self.id = id
        self.radius = -1
        self.label = None  # Will be initialized later
        self.edgeSet = []
        self.tree = []
        self.cross = []
        self.table = set()

    def combineEdgeSet(baseSet, addedSet):
        baseSet = baseSet.union(addedSet)

    def __repr__(self):
        return f"v{self.id}[L={self.label.label}]"