import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable
from Domain import Domain
from HashTable import HashTable
from CPT import CPT
from Node import Node


def Parser():
    tree = ET.parse("alarm.xml")
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
            # print "name of network == " + str(root[0].text)
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
                            # print "\n"
                    cp_tables.append(cpt)
                    Hash_CPT.put(cpt.name,cpt)
                    # print cpt
                    # print cpt.for_variable.name
                    # if cpt.given_variables is None:
                    #     print cpt.table
                    # else:
                    #     for t in xrange(0, len(cpt.given_variables)):
                    #         print "given: " + str(cpt.given_variables[t].name)
                    #     print cpt.table
                    # print ""
                    # print cpt.given_domain_sizes

    # print cp_tables

    Graph_nodes = []

    for i in xrange(0, len(variables)):
        n = Node(variables[i],Hash_CPT.get(variables[i].name))
        Hash_Nodes.put(n.name, n)
        Graph_nodes.append(n)

    for i in xrange(0, len(cp_tables)):
        connect(Graph_nodes, Hash_Nodes, cp_tables[i])


    # print Graph_nodes
    for i in xrange(0, len(Graph_nodes)):
        print Graph_nodes[i].name
        if Graph_nodes[i].children_nodes is None:
            print "no children"
        else:
            for j in xrange(0, len(Graph_nodes[i].children_nodes)):
                print "Child: " + str(Graph_nodes[i].children_nodes[j].name)
        print ""


def connect(Graph_nodes, Hash_Nodes, cpt):
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

def main():
    Parser()

if __name__ == '__main__':
  main()