import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable
from Domain import Domain
from HashTable import HashTable
from CPT import CPT


def Parser():
    tree = ET.parse("alarm.xml")
    root = tree.getroot()

    HTable = HashTable(67)

    variables = []

    if root.tag != "BIF":
        print "file must be xmlbif"
    else:
        root = root[0]
        if root.tag != "NETWORK":
            print "file must have a NETWORK tag"
        else:
            print "name of network == " + str(root[0].text)
            for i in xrange(1, len(root)):
                if root[i].tag == "VARIABLE":
                    # print "new RandomVariable(" + root[i][0].text + ")"
                    domain = getDomain(root[i])
                    rv = RandomVariable(root[i][0].text, domain)
                    variables.append(rv)
                    HTable.put(rv.name,rv)
                elif root[i].tag == "DEFINITION":
                    cpt = CPT()
                    for j in xrange(0, len(root[i])):
                        if root[i][j].tag == "FOR":
                            cpt.add_for_variable(HTable.get(root[i][j].text))
                        elif root[i][j].tag == "GIVEN":
                            cpt.add_given_variable(HTable.get(root[i][j].text))
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
                    # print cpt
                    print cpt.for_variable.name
                    if cpt.given_variables is None:
                        print cpt.table
                    else:
                        for t in xrange(0, len(cpt.given_variables)):
                            print "given: " + str(cpt.given_variables[t].name)
                        print cpt.table
                    print ""
                    # print cpt.given_domain_sizes


    # HTable.dump()
    # for i in xrange(0, len(variables)):
    #     print variables[i].domain.domain_list[0] == True

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