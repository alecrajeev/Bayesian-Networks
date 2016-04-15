from Domain import Domain

class RandomVariable(object):
    """
    This class is used to represent a single random variable.
    It will contain the name of the variable, and its domain.
    """

    def __init__(self, name, domain):
        self.name = name
        self.domain = domain