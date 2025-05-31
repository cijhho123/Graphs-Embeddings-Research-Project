""""
    Label:
        base  - integer (B(p)), base value
        level - integer (l(p))
        base_vertex - also related to the label w_p
"""


class Label:
    def __init__(self, graph, baseVertex, level=0):
        self.baseVertex = baseVertex  # vertex where label originated
        self.base = baseVertex.id     # b = ID of base vertex
        self.level = level            # l = depth from base
        self.label = graph.size * self.level + self.base  # P = n·l + b

    def promote(self, graph):
        """Returns a new label with level +1, same base."""
        return Label(graph, self.baseVertex, self.level + 1)

    @staticmethod
    def get_base(P, n):
        """Extract base from integer label P according to the paper."""
        return n if P % n == 0 else P % n

    @staticmethod
    def get_level(P, n):
        """Extract level from integer label P."""
        return P // n