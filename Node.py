

class Node(object):
    """
    This node will be represent a Node on the DAG. Each random variable will have a node
    """

    def __init__(self, random_variable, cpt):
        self.random_variable = random_variable
        self.name = self.random_variable.name
        self.cpt = cpt
        self.children_nodes = None

    def add_child(self, node):
        if self.children_nodes is None:
            self.children_nodes = []
        self.children_nodes.append(node)

