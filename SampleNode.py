

class SampleNode(object):
    """
    This node will represent a single variable's assinged value in an atomic event when doing a prior sample.
    The value will be what the random variable was assigned in this sample
    """

    def __init__(self, random_variable, cpt):
        self.random_variable = random_variable
        self.name = self.random_variable.name
        self.cpt = cpt
        self.value = None
        

