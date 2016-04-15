from SampleNode import SampleNode

class AtomicEvent(object):
    """
    This will represent a single atomic event when doing a prior sample.
    All of the random variables will be assigned values.
    """

    def __init__(self, Graph):
        self.sample_nodes = [None]*len(Graph)
        for i in xrange(0, len(Graph)):
            self.sample_nodes[i] = SampleNode(Graph[i].random_variable, Graph[i].cpt)

