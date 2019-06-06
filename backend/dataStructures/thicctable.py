from objectSaver import save, load

class Thicctable():
    """
    Class to store indexed webdata in two branches:
        -Knowledge Branch: Maps knowledge tokens to indexed, relevant list
        -Concept Branch: Maps page clusters to indexed list of cluster contents
    Methods:
        -Insert: Add value to list associated with
    """

    def __init__(self, knowledgeKeys=[], conceptKeys=[]):
        """ Initialize both branches as stores mapping keys to empty lists """
        self.knowledgeBranch = {key:[] for key in knowledgeKeys}
        self.conceptBranch = {key:[] for key in conceptKeys}

    def knowledge_insert(self, key, (score, info)):
        """ Add value to key in knowledgeBranch"""
        self.knowledgeBranch[key].append((score, info))

    def knowledge_insert(self, key, (score, info)):
        """ Add value to key in conceptBranch """
        self.conceptBranch[key].append((score, info))

    def sort_branch(self, branch, rankAlgo):
        """ Applies page ranking algorithm to rank pages for every key in branch """
        # assert valid branch
        assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
        # define root
        root = self.knowledgeBranch if (branch=='knowledge') else self.conceptBranch
        # apply ranking algorithm to every value in key, value store
        rankLambda = lambda key : rankAlgo(key, root[key])
        root = dict(map(rankLambda, root))
        # store ranked root in knowledge or conceptBranch
        if (branch=='knowledge'):
            self.knowledgeBranch = root
        else:
            self.conceptBranch = root

    def search(self, branch, key, numPages=20):
        """
        Pops top numPages pages from valueList mapped from key in branch
        Built for speed, not readability
        """
        if branch=="knowledge":
            return self.knowledgeBranch[key][:numPages]
        elif branch=="concept":
            return self.conceptBranch[key][:numPages]
        else:
            raise ValueError("Invalid Branch")

    def metrics(self, branch):
        """ Display metrics for every page in a branch """
        # assert valid branch
        assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
        # define root
        root = self.knowledgeBranch if (branch=='knowledge') else self.conceptBranch
        # query branch metrics
        for key in root:
            print(f"Key: {key}\n\tNumber of Pages: {len(root[key])}")
        return True

# Testing

import numpy as np

knowledgeSet = load("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")

print("Loaded")

x = Thicctable(knowledgeKeys=knowledgeSet)

print("x init")

for _ in range(10000000):
    key = 'harvard'
    value = np.random.choice([0, 1, 2], size=1)
    x.insert(key, value[0], True)

print('added')

import time
start = time.time()
result = x.search('knowledge', 'hi')
end = time.time()
print(f"Queried in: {end - start}")
print(result)
