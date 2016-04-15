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

    def check_evidence(self, variable_name, variable_value):
        """
        This will return True if the event accepts a piece of evidence.
        Will return False if a sample has a value that doesn't correspond to the evidence.
        """
        for i in xrange(0, len(self.sample_nodes)):
            if self.sample_nodes[i].name == variable_name:
                if self.sample_nodes[i].value == variable_value:
                    return True
                else:
                    return False

        print "whoops, I guess the evidence variable was not assigned in the event"
        return None

    def get_domain_value_index(self, i):
        """
        This returns the index of query variable's value in its domain.
        i is the index of the query variable in sample_nodes
        """
        for j in xrange(0, len(self.sample_nodes[i].random_variable.domain.domain_list)):
            if self.sample_nodes[i].random_variable.domain.domain_list[j] == self.sample_nodes[i].value:
                return j

        print "whoops, looks like the assigned value is not in the domain of the query variable"
        return None


