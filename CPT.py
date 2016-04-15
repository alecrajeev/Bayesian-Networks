import numpy as np
from Domain import Domain
from RandomVariable import RandomVariable
from itertools import product

class CPT(object):
    """
    This class is used to represent a Conditional Probability Table
    for_variable is a RandomVariable that is the for or query
    given_variables is a list that represents the list of given given_variables
    given_domain_sizes is a list of sizes of domains for the given given_variables

    table is the actual conditional probability table.
    It will have the number of rows corresponding to all the possible combinations
    of values that the given variables can take.
    It will have the number of columns representing all the possible values that the
    for variable can take.
    When numbers are being inputted it assumes that the probablities are given in the
     order that the original random variable listed its outcomes.
    """

    def __init__(self):
        self.for_variable = None
        self.name = None
        self.for_size = 0
        self.given_variables = None
        self.given_domain_sizes = None
        self.table = None
        self.helper_table = None

    def add_for_variable(self, for_variable):
        """
        Adds the for variable for this condiontional probability table.
        """
        self.for_variable = for_variable
        self.name = for_variable.name
        self.for_size = self.for_variable.domain.size

    def add_given_variable(self, given_variable):
        """
        This will add the list of given variables for this condiontional probability table.
        """
        if self.given_variables is None:
            self.given_variables = []
        self.given_variables.append(given_variable)
        if self.given_domain_sizes is None:
            self.given_domain_sizes = []
        self.given_domain_sizes.append(given_variable.domain.size)

    def build_table(self):
        """
        This build the condiontional probability table.
        It also builds a helper table that represnts the values of the given 
        variables for each row. This helper table is built with itertools.
        """
        if self.given_variables is None:
            self.table = np.full((1, self.for_size),-1.0, dtype=np.float_)
        else:
            n = 1
            for k in xrange(0, len(self.given_domain_sizes)):
                if self.given_domain_sizes[k] == 0:
                    print "problem in the domain sizes"
                n *= self.given_domain_sizes[k]

            self.helper_table = [None]*n

            helper_domain = []

            for i in xrange(0, len(self.given_variables)):
                helper_domain.append(self.given_variables[i].domain.domain_list)

            helper_iter = list(product(*helper_domain))
            for i in xrange(0, len(self.helper_table)):
                self.helper_table[i] = list(helper_iter[i])

            self.table = np.full((n,self.for_size),-1.0, dtype=np.float_)

    def add_prob(self, p):
        """
        Adds the probability from the parsed table to the conditional probability table.
        """

        for i in xrange(0, np.shape(self.table)[0]):
            for j in xrange(0, np.shape(self.table)[1]):
                if self.table[i][j] == -1.0:
                    self.table[i][j] = p
                    return True
        print "woah the table is full"

    def get_sample_value(self, parent_values):
        """
        This finds the conditional probability given the parents,
        and then assigns a random value based upon the probability.
        """
        if len(parent_values) == 0:
            # if this variable has no givens
            if not(self.given_variables is None):
                print "whoops, need parent variable values"
            else:
                prob = self.table[0]
                return self.get_assigned_variable(prob)
        else:
            if self.given_variables is None:
                # if there are prior assigned values, but this variable has no givens
                prob = self.table[0]
                return self.get_assigned_variable(prob)
            else:
                given_v_index = self.get_given_index(parent_values)
                prob = self.table[given_v_index]
                return self.get_assigned_variable(prob)


    def get_assigned_variable(self, prob):
        """
        This returns the randomly assigned variable. The probability of getting this outcome corresponds
        to the condiontional probability table.
        """
        choice = np.random.choice(self.for_variable.domain.domain_list, 1, p=prob)
        return choice[0]

    def get_prob(self, evidence_values):
        """
        This gives the condiontional probability given the evidence_values.
        """
        for_v = []
        for i in xrange(0, len(evidence_values)):
            if self.name == evidence_values[i][0]:
                for_v = evidence_values[i]

        for_v_index = self.get_index(for_v[1])

        if self.given_variables is None:
            return self.table[0][for_v_index]
        else:
            given_v_index = self.get_given_index(evidence_values)
            
            return self.table[given_v_index, for_v_index]

        return .7

    def get_index(self, val):
        """
        It returns the index of the for_variable's domain that has the corresponding outcome.
        """
        for i in xrange(0, self.for_variable.domain.size):
            if val == self.for_variable.domain.domain_list[i]:
                return i
        print "whoops, value for evidence is not in domain"

    def get_given_index(self, evidence_values):
        """
        This gives which row of the conditional probability table corresponds to the given variables assigned values.
        These assigned values come either from prior sampling or the evidence.
        It uses the helper table to do this.
        """

        if self.check_given_variables_needed(evidence_values):
            print "whoops, not in topological order or something. Required given variable is not included"
            return None

        given_values = [None]*len(self.given_variables)
        for i in xrange(0, len(given_values)):
            given_values[i] = self.get_evidence_val(self.given_variables[i].name, evidence_values)

        for i in xrange(0, len(self.helper_table)):
            if self.check_helper(given_values, i):
                return i

    def check_given_variables_needed(self, evidence_values):
        """
        This assumes that the given variable is initially not in the evidence_values.
        Then it cycles through each given variable and checks if it's in the evidence_values.
        If any given variable is not included, it returns False.
        Otherwise returns true.
        """

        for i in xrange(0, len(self.given_variables)):
            g = self.given_variables[i].name
            g_included = False
            for j in xrange(0, len(evidence_values)):
                if g == evidence_values[i][0]:
                    g_included = True
            if not(g_included):
                return False
        return True


    def get_evidence_val(self, name, evidence_values):
        for i in xrange(0, len(evidence_values)):
            if evidence_values[i][0] == name:
                return evidence_values[i][1]
        print "whoops, there should be an evidence that there isn't"
        return 1000

    def check_helper(self, given_values, i):
        """
        Checks if any of the given variables that should have values don't.
        """
        
        for j in xrange(0, len(self.helper_table[i])):
            if self.helper_table[i][j] != given_values[j]:
                return False
        return True











