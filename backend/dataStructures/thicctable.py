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
        branch = branch.lower()
        # assert valid branch
        assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
        # query branch metrics
        if (branch=='knowledge'):
        else:


x = Thicctable(knowledgeKeys=['hi','hello','yo'])

import numpy as np

for _ in range(10000):
    key = np.random.choice(['hi', 'hello', 'yo'], size=1)
    x.insert(key[0], 'html', True)

print(x.knowledgeBranch)
