from objectSaver import save, load

class Thicctable():
    """
    Class to store indexed webdata as keys mapping to dict of page data
    Methods:
        -Insert: Add value to list associated with
    """

    def __init__(self, keys):
        """
        Initialize branch as store mapping keys to empty lists.
        Keys should cover all buckets of dict, but can be added or removed
        """
        self.topDict = {key:[] for key in keys}

    def add_key(self, key):
        """ Adds key and corresponding empty list to topDict """
        self.topDict.update({key:[]})

    def remove_key(self, key):
        """ Removes key and associate list from topDict """
        del self.topDict[key]

    # def insert(self, key, ):
    #     """ Add value to key in knowledgeBranch"""
    #     self.topDict[key].append((score, info))
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
