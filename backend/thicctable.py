class Store():
    """ Test class composed of list to which pageDicts are added """
    def __init__(self):
        self.data = []
    def add(self, elt):
        self.data += [(elt)]

class Metrics():
    """ Class to keep track of scrape progress """
    def __init__(self):
        self.count = 0
        self.errors = 0

    def add(self, error=False):
        self.count += 1
        if error:
            self.errors += 1
