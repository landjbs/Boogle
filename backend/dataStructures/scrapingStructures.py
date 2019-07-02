"""
Defines threadsafe data structures for temporary storage of information during
multithreraded webcrawling.
"""

import json

class Simple_List():
    """ Class reimplementing list for easy threading """
    def __init__(self):
        self.data = []

    def clear(self):
        self.data = []

    def add(self, elt):
        """ Adds element to data list """
        self.data.append(elt)

    def save(self, outPath):
        with open(f"{outPath}.json", 'w+', encoding="utf-8") as FileObj:
            json.dump(self.data, FileObj)
        return True

    def load(self, inPath):
        with open(f"{inPath}.json", 'r') as FileObj:
            self.data = json.load(FileObj)
        return True

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
