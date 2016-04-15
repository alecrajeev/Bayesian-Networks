import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable
from Domain import Domain
from HashTable import HashTable
from CPT import CPT
from Node import Node
import copy
import sys

def exact_inference(input_values, Graph, Hash_Nodes):
    """
    This implements the exact inference algorithm that uses enumeration.
    It returns a posterior distribution over the query variable for every
    outcome of the query variable. This probability is normalized.
    It takes in the evidence from input values. The Graph is built
    from a previous function with the parser.
    """

    evidence_values = []

    # formats the evidence into a list
    ecount = 1
    while ecount < (len(input_values)-1):
        evidence_values.append([input_values[ecount],input_values[ecount+1]])
        ecount += 2

    # finds the query_variable random variable from the name of the variable.
    query = input_values[0]
    query_variable = None
    for i in xrange(0, len(Graph)):
        if Graph[i].name == query:
            query_variable = Graph[i].random_variable

    # grabs a list of variables in topological order from the Graph
    variables_list = []
    for i in xrange(0, len(Graph)):
        variables_list.append(Graph[i].random_variable)

    posterior_distribution = [None]*query_variable.domain.size

    # cycles through every possible outcome of the query variable
    # finds the unnormalized probability if you add one specific value
    # of the query variable as evidence
    for i in xrange(0, query_variable.domain.size):
        evidence_values.append([query_variable.name, query_variable.domain.domain_list[i]])
        en = enumerate(variables_list, evidence_values, Graph, Hash_Nodes)
        evidence_values.pop()
        # once the probability is found, it deletes that additional piece of evidence
        posterior_distribution[i] = en

    posterior_distribution = np.array(posterior_distribution)

    sum = np.sum(posterior_distribution)

    # alpha normailizes everything
    alpha = 1.0/sum

    print "Query Variable: " + str(query_variable.name)
    print query_variable.domain.domain_list
    print posterior_distribution*alpha
    return posterior_distribution

def enumerate(variables_list, evidence_values, Graph, Hash_Nodes):
    """
    This implements the enumerate-all part of the inference by enumeration algorithm.
    It returns a real number that represents the unnormalized probability for 
    that outcome of the query variable. This is a recursive algorithm.
    """
    if len(variables_list) == 0:
        # returns 1.0 if there are no more variables.
        return 1.0
    Y = variables_list[0]
    # Y is the first variable on the list

    y = grab_y(Y, evidence_values)
    if check_Y(Y, y, evidence_values):
        p = get_conditional_probability(Y, evidence_values, Graph, Hash_Nodes)
        rest_variables = variables_list[1:len(variables_list)]
        # these are the rest of the variables. (skips element 0)
        return p * enumerate(rest_variables, evidence_values, Graph, Hash_Nodes)
    else:
        sum = 0.0
        # cycle through to all values in Y's domain
        for i in xrange(0, Y.domain.size):
            # the additional evidence where you extend Y = y
            additional_evidence = copy.deepcopy(evidence_values)
            additional_evidence.append([Y.name, Y.domain.domain_list[i]])
            p = get_conditional_probability(Y, additional_evidence, Graph, Hash_Nodes)
            rest_variables = variables_list[1:len(variables_list)]
            # this finds the sum of the conditional probability for every value of Y
            sum += p * enumerate(rest_variables, additional_evidence, Graph, Hash_Nodes)
        return sum

def get_conditional_probability(Y, evidence_values, Graph, Hash_Nodes):
    """
    Given the evidence values and the Graph, what is the conditional probability
    of the random variable Y.
    """

    node = Hash_Nodes.get(Y.name)
    cpt = node.cpt
    p = cpt.get_prob(evidence_values)

    return p


def grab_y(Y, evidence_values):
    """
    This returns the value for Y in the evidence or
    just Y's first value if it's not in the evidence
    """
    for i in xrange(0, len(evidence_values)):
        if Y.name == evidence_values[i][0]:
            return evidence_values[i][1]
    return Y.domain.domain_list[0]

def check_Y(Y, y, evidence_values):
    """
    This checks if the random variable Y is in the evidence
    """
    for i in xrange(0, len(evidence_values)):
        if Y.name == evidence_values[i][0] and y == evidence_values[i][1]:
            return True

    return False


def build_graph(variables, Hash_CPT, cp_tables, Hash_Nodes):
    """
    This builds the Graph. It creates a Node for each random variable.
    Each Node also gets that random variables' conditional probability table.
    Then it sorts the Graph with a topological sort.
    """
    Graph = []

    for i in xrange(0, len(variables)):
        n = Node(variables[i],Hash_CPT.get(variables[i].name))
        Hash_Nodes.put(n.name, n)
        Graph.append(n)

    for i in xrange(0, len(cp_tables)):
        connect(Hash_Nodes, cp_tables[i])

    sorted_nodes = []

    while(check_unmarked(Graph)):
        for i in xrange(0, len(Graph)):
            if Graph[i].perm_mark == 0:
                topological_visit(Graph[i], sorted_nodes)
                break

    # the actualy append() function sorts them in reverse, so must reverse that.
    sorted_nodes.reverse()

    Graph = sorted_nodes

    return Graph

def Parser(file_name):
    """
    Parses the xmlbif file and builds the list of variables.
    Also builds the list condiotional probability tables.
    Also couple hash tables are built to quickly access things.
    """
    tree = ET.parse(file_name)
    root = tree.getroot()

    n_prime = 67

    Hash_Variables = HashTable(n_prime)
    Hash_CPT = HashTable(n_prime)
    Hash_Nodes = HashTable(n_prime)

    variables = []
    cp_tables = []

    if root.tag != "BIF":
        print "file must be xmlbif"
    else:
        root = root[0]
        if root.tag != "NETWORK":
            print "file must have a NETWORK tag"
        else:
            for i in xrange(1, len(root)):
                if root[i].tag == "VARIABLE":
                    domain = getDomain(root[i])
                    rv = RandomVariable(root[i][0].text, domain)
                    variables.append(rv)
                    Hash_Variables.put(rv.name,rv)
                elif root[i].tag == "DEFINITION":
                    cpt = CPT()
                    for j in xrange(0, len(root[i])):
                        if root[i][j].tag == "FOR":
                            cpt.add_for_variable(Hash_Variables.get(root[i][j].text))
                        elif root[i][j].tag == "GIVEN":
                            cpt.add_given_variable(Hash_Variables.get(root[i][j].text))
                        elif root[i][j].tag == "TABLE":
                            cpt.build_table()
                            split_text = root[i][j].text.split(" ")
                            for t in xrange(0, len(split_text)):
                                try:
                                    p = float(split_text[t])
                                    cpt.add_prob(p)
                                except ValueError:
                                    ad = 3
                    cp_tables.append(cpt)
                    Hash_CPT.put(cpt.name,cpt)

    return variables, cp_tables, Hash_Variables, Hash_CPT, Hash_Nodes

def print_cpt(cpt):
    """
    Prints the conditional probability table
    """
    print cpt
    print cpt.for_variable.name
    if cpt.given_variables is None:
        print cpt.table
    else:
        for t in xrange(0, len(cpt.given_variables)):
            print "given: " + str(cpt.given_variables[t].name)
        print cpt.table
    print ""
    print cpt.given_domain_sizes

def print_graph(Graph):
    """
    Prints the graph. Prints each nodes and it's children
    """
    for i in xrange(0, len(Graph)):
        print Graph[i].name
        if Graph[i].children_nodes is None:
            print "no children"
        else:
            for j in xrange(0, len(Graph[i].children_nodes)):
                print "Child: " + str(Graph[i].children_nodes[j].name)
        print ""

def topological_visit(node, sorted_nodes):
    """
    Uses depth first search to do a topological sort
    """
    if node.temp_mark == 1:
        print "Graph not DAG"
        return None
    if node.perm_mark == 0:
        node.temp_mark = 1
        if not(node.children_nodes is None):
            for i in xrange(0, len(node.children_nodes)):
                topological_visit(node.children_nodes[i], sorted_nodes)
        node.perm_mark = 1
        node.temp_mark = 0
        sorted_nodes.append(node)


def check_unmarked(Graph):
    """
    Checked if permanently mark is false. Used in topololgical sort
    """
    for i in xrange(0, len(Graph)):
        if Graph[i].perm_mark == 0:
            return True

    return False

def connect(Hash_Nodes, cpt):
    """
    Connects the children nodes to the parents.
    A variable that has givens will be the children of the givens.
    """
    if cpt.given_variables is None:
        # node has no givens, is a root node
        return 1

    for i in xrange(0, len(cpt.given_variables)):
        n = cpt.given_variables[i]
        Hash_Nodes.get(n.name).add_child(Hash_Nodes.get(cpt.name))

def getDomain(branch):
    """
    Parses and stores all the possible outcomes of a Random Variable.
    """
    domain = Domain()

    for i in xrange(0, len(branch)):
        if branch[i].tag == "OUTCOME":
            domain.add_to_domain(branch[i].text)
            
    return domain

def format_input(input_values):
    """
    This takes the command line arguments and splits them up into
    more manageable parts.
    """
    input_values = input_values[2:len(input_values)]
    for i in xrange(0, len(input_values)):
        if input_values[i] == "True" or input_values[i] == "true":
            input_values[i] = True
        elif input_values[i] == "False" or input_values[i] == "false":
            input_values[i] = False

    return input_values

def main():
    input_values = format_input(sys.argv)
    variables, cp_tables, Hash_Variables, Hash_CPT, Hash_Nodes = Parser(sys.argv[1])
    Graph = build_graph(variables, Hash_CPT, cp_tables, Hash_Nodes)
    posterior_distribution = exact_inference(input_values, Graph, Hash_Nodes)


if __name__ == '__main__':
  main()