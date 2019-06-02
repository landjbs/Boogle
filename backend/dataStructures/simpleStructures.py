# Defines class for wide column store of web data gathered in crawler.py
####### TO BE UPDATED ########

class Simple():
    """ Class reimplementing list for easy threading """
    def __init__(self):
        self.data = []

    def add(self, elt):
        """ Adds element to data list """
        self.data.append(elt)

    def to_csv(self, path, sep=","):
        """ Saves dict list as csv in path """
        file = open(path, "w+")
        for line in self.data:
            for attribute in line:
                file.write(attribute + sep)
            file.write("\n")
        print(f"File saved to {path} | Delimeter: '{sep}'")

class Metrics():
    """ Class to keep track of scrape progress """
    def __init__(self):
        self.count = 0
        self.errors = 0

    def add(self, error=False):
        self.count += 1
        if error:
            self.errors += 1
