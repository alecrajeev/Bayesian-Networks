import numpy as np
import xml.etree.ElementTree as ET
from RandomVariable import RandomVariable

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
                    print "new RandomVariable(" + root[0][i][0].text + ")"
                    outcomes = getOutcomes(root[0][i])
                    rv = RandomVariable(root[0][i][0].text, outcomes)
                    variables.append(rv)

    for i in xrange(0, len(variables)):
        print variables[i]

def getOutcomes(branch):
    outcomes = []
    for i in xrange(0, len(branch)):
        if branch[i].tag == "OUTCOME":
            if branch[i].text == "true" or branch[i].text == "True":
                outcomes.append(True)
            elif branch[i].text == "false" or branch[i].text == "False":
                outcomes.append(False)
            else:
                outcomes.append(branch[i].text)
    print "outcomes == " + str(outcomes)
    return outcomes

def main():
    Parser()

if __name__ == '__main__':
  main()