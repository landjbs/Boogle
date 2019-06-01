# Defines class for wide column store of web data gathered in crawler.py
####### TO BE UPDATED ########

class Simple():
    """ Class reimplementing list for easy threading """
    def __init__(self):
        self.data = []

    def add(self, elt):
        self.data.append(elt)

class Metrics():
    """ Class to keep track of scrape progress """
    def __init__(self):
        self.count = 0
        self.errors = 0

    def add(self, error=False):
        self.count += 1
        if error:
            self.errors += 1
