import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable
from Domain import Domain


def Parser():
    tree = ET.parse("alarm.xml")
    root = tree.getroot()

    variables = []

    if root.tag != "BIF":
        print "file must be xmlbif"
    else:
        if root[0].tag != "NETWORK":
            print "file must have a NETWORK tag"
        else:
            print "name of network == " + str(root[0][0].text)
            for i in xrange(1, len(root[0])):
                if root[0][i].tag == "VARIABLE":
                    # print "new RandomVariable(" + root[0][i][0].text + ")"
                    domain = getDomain(root[0][i])
                    rv = RandomVariable(root[0][i][0].text, domain)
                    variables.append(rv)
                elif root[0][i].tag == "DEFINITION":
                    print "definition"

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