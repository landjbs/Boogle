from objectSaver import save, load

class Thicctable():
    """
    Class to store indexed webdata as keys mapping to list of tuples of page data
    in format (score, title, url, keywords, head)
    Methods:
        -__init__: Build topDict mapping list of keys to empty list
        -add_key: Adds key mapping to an empty list to the topDict
        -remove_key: Removes a key and the corresponding list from the topDict
        -
    """

    def __init__(self, keys):
        """ Initialize branch as key-val store mapping keys to empty lists """
        self.topDict = {key:[] for key in keys}

    def add_key(self, key):
        """ Adds key and corresponding empty list to topDict """
        self.topDict.update({key:[]})

    def remove_key(self, key):
        """ Removes key and associate list from topDict """
        del self.topDict[key]

    def clean_key(self, key):
        """
        Clears the list associated with a key in the topDict
        Same funcitonality as clip_key(key, 0).
        """
        self.topDict[key] = []

    def clip_key(self, key, n):
        """ Clips list mapped by key to n elements """
        self.topDict[key] = self.topDict[key][:n]

    def insert_value(self, key, value):
        """ Adds value to the list mapped by key in topDict """
        self.topDict[key].append(value)

    def remove_value(self, key, value)

    #
    # def sort_branch(self, branch):
    #     """ Applies page ranking algorithm to rank pages for every key in branch """
    #     # assert valid branch
    #     assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
    #     # define root
    #     root = self.knowledgeBranch if (branch=='knowledge') else self.conceptBranch
    #     # define lambda for sorting branches
    #     # sortLambda = lambda key : root[key].sort()
    #     # apply ranking algorithm to every value in key, value store
    #     # root = dict(map(sortLambda, root))
    #     for key in root:
    #         root[key].sort()
    #     # store ranked root in knowledge or conceptBranch
    #     if (branch=='knowledge'):
    #         self.knowledgeBranch = root
    #     else:
    #         self.conceptBranch = root
    #
    # def search(self, branch, key, numPages=20):
    #     """
    #     Pops top numPages pages from valueList mapped from key in branch
    #     Built for speed, not readability
    #     """
    #     if branch=="knowledge":
    #         return self.knowledgeBranch[key][:numPages]
    #     elif branch=="concept":
    #         return self.conceptBranch[key][:numPages]
    #     else:
    #         raise ValueError("Invalid Branch")
    #
    # def metrics(self, branch):
    #     """ Display metrics for every page in a branch """
    #     # assert valid branch
    #     assert (branch in ['knowledge', 'concept']), "Valid branches are 'knowledge' or 'concept'"
    #     # define root
    #     root = self.knowledgeBranch if (branch=='knowledge') else self.conceptBranch
    #     # query branch metrics
    #     for key in root:
    #         print(f"Key: {key}\n\tNumber of Pages: {len(root[key])}")
    #     return True

# Testing
#

x = Thicctable(keys=['a','b','c'])

x.add_key('d')

x.remove_key('a')

x.insert('b', 2)

x.clean_key('b')

x.insert('d', 1)

x.insert('d', 2)

x.insert('d', 3)

x.insert('d', 4)

x.clip_key('d', 0)

print(x.topDict)

# import numpy as np
#
# # knowledgeSet = load("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")
#
# # x = Thicctable(knowledgeKeys=knowledgeSet)
# x = Thicctable(knowledgeKeys=['harvard'])
#
# print("x init")
#
# for _ in range(10):
#     key = 'harvard'
#     score = np.random.choice([0, 1, 2], size=1)
#     value = np.random.choice(['a','b'], size=1)
#     x.knowledge_insert(key, score[0], value[0])
#
# print('added')
#
# x.sort_branch('knowledge')
#
# print(x.search('knowledge', 'harvard'))





pass
