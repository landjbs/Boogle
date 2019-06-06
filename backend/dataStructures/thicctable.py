from objectSaver import save, load

class Thicctable():
    """
    Class to store indexed webdata in two branches:
        -Knowledge Branch: Maps knowledge tokens to indexed, relevant list
        -Concept Branch: Maps page clusters to indexed cluster contents
    Methods:
        -Insert: Add a webpage to a branch
    """

    def __init__(self, knowledgeKeys=[], conceptKeys=[]):
        """ Initialize both branches as stores mapping keys to empy lists """
        self.knowledgeBranch = {key:[] for key in knowledgeKeys}
        self.conceptBranch = {key:[] for key in conceptKeys}

    def insert(self, key, value, knowledge):
        """ """
        if knowledge:
            self.knowledgeBranch[key].append(value)
        else:
            self.conceptBranch[key].append(value)

    def metrics(self, branch):
        """ Display metrics """
        branch = branch.lower()
        # assert valid branch
        assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
        # query branch metrics
        root = self.knowledgeBranch if (branch=='knowledge') else self.conceptBranch
        for key in root:
            print(f"Key: {key}\n\tNumber of Pages: {len(root[key])}")
        return True

# Testing

import time
import numpy as np


loadStart = time.time()

knowledgeSet = load("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")

loadEnd = time.time()

print(f"Loaded in {loadEnd - loadStart} seconds")

createStart = time.time()

x = Thicctable(knowledgeKeys=knowledgeSet)

createEnd = time.time()

print(f"Created in {createEnd - createStart} seconds")

addStart = time.time()

for _ in range(10000):
    key = np.random.choice(['hi', 'hello', 'yo'], size=1)
    x.insert(key[0], 'html', True)

addEnd = time.time()

print(f"Added in {addEnd - addStart} seconds")

x.metrics('knowledge')
