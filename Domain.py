

class Domain(object):
    """
    A Domain represents an ordered set of possible Values for a Variable.
    """

    def __init__(self):
        self.size = 0
        self.domain_list = []

    def add_to_domain(self, outcome):
        self.size += 1
        if outcome == "true" or outcome == "True":
            self.domain_list.append(True)
        elif outcome == "false" or outcome == "False":
            self.domain_list.append(False)
        else:
            self.domain_list.append(outcome)
