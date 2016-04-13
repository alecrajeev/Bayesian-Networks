import numpy as np
from Domain import Domain
from RandomVariable import RandomVariable

class CPT(object):
    """
    This class is used to represent a Conditional Probability Table
    for_variable is a RandomVariable that is the for or query
    given_variables is a list that represents the list of given given_variables
    given_domain_sizes is a list of sizes of domains for the given given_variables

    table is the actual conditional probability table. It will have the number of rows corresponding to all the possible combinations of values that the given variables can take. It will have the number of columns representing all the possible values that the for variable can take. When numbers are being inputted it assumes that the probablities are given in the order that the original random variable listed its outcomes.
    """

    def __init__(self):
        self.for_variable = None
        self.name = None
        self.for_size = 0
        self.given_variables = None
        self.given_domain_sizes = None
        self.table = None

    def add_for_variable(self, for_variable):
        self.for_variable = for_variable
        self.name = for_variable.name
        self.for_size = self.for_variable.domain.size

    def add_given_variable(self, given_variable):
        if self.given_variables is None:
            self.given_variables = []
        self.given_variables.append(given_variable)
        if self.given_domain_sizes is None:
            self.given_domain_sizes = []
        self.given_domain_sizes.append(given_variable.domain.size)

    def build_table(self):
        if self.given_variables is None:
            self.table = np.full((1, self.for_size),-1.0, dtype=np.float_)
        else:
            n = 1
            for k in xrange(0, len(self.given_domain_sizes)):
                if self.given_domain_sizes[k] == 0:
                    print "problem in the domain sizes"
                n *= self.given_domain_sizes[k]
            
            self.table = np.full((n,self.for_size),-1.0, dtype=np.float_)

    def add_prob(self, p):

        for i in xrange(0, np.shape(self.table)[0]):
            for j in xrange(0, np.shape(self.table)[1]):
                if self.table[i][j] == -1.0:
                    self.table[i][j] = p
                    return True
        print "woah the table is full"











