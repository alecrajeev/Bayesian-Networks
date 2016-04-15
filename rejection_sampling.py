import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable
from Domain import Domain
from HashTable import HashTable
from CPT import CPT
from Node import Node
from AtomicEvent import AtomicEvent
import copy
import sys

def rejection_sampling(input_values, Graph, Hash_Nodes, N):

    evidence_values = []
    ecount = 1
    while ecount < (len(input_values)-1):
        evidence_values.append([input_values[ecount],input_values[ecount+1]])
        ecount += 2

    query = input_values[0]
    query_variable = None
    for i in xrange(0, len(Graph)):
        if Graph[i].name == query:
            query_variable = Graph[i].random_variable


    atomic_event_list = [None]*N

    # all 1000 events get randomly assigned
    for i in xrange(0, N):
        event = AtomicEvent(Graph)
        prior_sampling(event)
        atomic_event_list[i] = event

    accept_list = []

    for i in xrange(0, N):
        event = atomic_event_list[i]
        if accepted_event(event, evidence_values):
            accept_list.append(event)

    samples_count_per_outcome = np.zeros(query_variable.domain.size, dtype=np.int32)
    for i in xrange(0, len(accept_list)):
        update_count(samples_count_per_outcome, accept_list[i], query_variable)

    print "Query Variable: " + str(query_variable.name)
    print query_variable.domain.domain_list
    print samples_count_per_outcome/float(np.sum(samples_count_per_outcome))

def prior_sampling(event):
    """
    This assigns each variable a value based upon it's conditional probability randomly
    """

    # equivalent to evidence_values
    parent_values = []

    for i in xrange(0, len(event.sample_nodes)):
        sample = event.sample_nodes[i]
        sample.assign_random_value(parent_values)

def update_count(samples_count_per_outcome, accepted_event, query_variable):
    for i in xrange(0, len(accepted_event.sample_nodes)):
        if accepted_event.sample_nodes[i].name == query_variable.name:
            j = accepted_event.get_domain_value_index(i)
            samples_count_per_outcome[j] += 1

def accepted_event(event, evidence_values):
    """
    This returns True all the evidence corresponds to the values assigned in the event.
    It returns False if one of the evidence values is different from the assigned value.
    """

    for i in xrange(0, len(evidence_values)):
        if not(event.check_evidence(evidence_values[i][0],evidence_values[i][1])):
            return False

    return True



def get_conditional_probability(Y, evidence_values, Graph, Hash_Nodes):
    node = Hash_Nodes.get(Y.name)
    cpt = node.cpt
    p = cpt.get_prob(evidence_values)

    return p


def grab_y(Y, evidence_values):
    """
    this returns the value for Y in the evidnce or
    just Y's first value if it's not in the evidence
    """
    for i in xrange(0, len(evidence_values)):
        if Y.name == evidence_values[i][0]:
            return evidence_values[i][1]
    return Y.domain.domain_list[0]

def check_Y(Y, y, evidence_values):
    """
    this checks if the random variable Y is in the evidence
    """
    for i in xrange(0, len(evidence_values)):
        if Y.name == evidence_values[i][0] and y == evidence_values[i][1]:
            return True

    return False


def build_graph(variables, Hash_CPT, cp_tables, Hash_Nodes):
    Graph = []

    for i in xrange(0, len(variables)):
        n = Node(variables[i],Hash_CPT.get(variables[i].name))
        Hash_Nodes.put(n.name, n)
        Graph.append(n)

    for i in xrange(0, len(cp_tables)):
        connect(Hash_Nodes, cp_tables[i])

    # print_graph(Graph)

    sorted_nodes = []

    # topological sort

    while(check_unmarked(Graph)):
        for i in xrange(0, len(Graph)):
            if Graph[i].perm_mark == 0:
                topological_visit(Graph[i], sorted_nodes)
                break

    sorted_nodes.reverse()

    Graph = sorted_nodes

    # print_graph(Graph)

    return Graph

def Parser(file_name):
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
    for i in xrange(0, len(Graph)):
        print Graph[i].name
        if Graph[i].children_nodes is None:
            print "no children"
        else:
            for j in xrange(0, len(Graph[i].children_nodes)):
                print "Child: " + str(Graph[i].children_nodes[j].name)
        print ""

def topological_visit(node, sorted_nodes):
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
    for i in xrange(0, len(Graph)):
        if Graph[i].perm_mark == 0:
            return True

    return False

def connect(Hash_Nodes, cpt):
    if cpt.given_variables is None:
        # node has no givens, is a root node
        return 1

    for i in xrange(0, len(cpt.given_variables)):
        n = cpt.given_variables[i]
        Hash_Nodes.get(n.name).add_child(Hash_Nodes.get(cpt.name))

def getDomain(branch):
    domain = Domain()

    for i in xrange(0, len(branch)):
        if branch[i].tag == "OUTCOME":
            domain.add_to_domain(branch[i].text)
            
    return domain

def format_input(input_values):
    input_values = input_values[3:len(input_values)]
    for i in xrange(0, len(input_values)):
        if input_values[i] == "True" or input_values[i] == "true":
            input_values[i] = True
        elif input_values[i] == "False" or input_values[i] == "false":
            input_values[i] = False

    return input_values

def main():
    input_values = format_input(sys.argv)
    variables, cp_tables, Hash_Variables, Hash_CPT, Hash_Nodes = Parser(sys.argv[2])
    Graph = build_graph(variables, Hash_CPT, cp_tables, Hash_Nodes)
    rejection_sampling(input_values, Graph, Hash_Nodes, int(sys.argv[1]))

if __name__ == '__main__':
  main()