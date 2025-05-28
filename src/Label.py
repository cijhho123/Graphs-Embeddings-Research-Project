""""
    Label:
        base  - integer (B(p)), base value
        level - integer (l(p))
        base_vertex - also related to the label w_p
"""


class Label:
    # TODO empty. 
    def __init__(self, graph, label, vertex):
        self.label = label
        self.base = self.generateBaseValue(graph, vertex)
        self.level = 0
        self.baseVertex = vertex

    def generateBaseValue(self, graph, v):   
        size = graph.size  # n
        if size % v.label == 0:
            v.label.base = size
        else:
            v.label.base = (v.label % size)