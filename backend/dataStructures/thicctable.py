from objectSaver import save, load

class Thicctable():
    """
    Class to store indexed webdata as keys mapping to list of tuples of page data
    in format (score, domainReverse, url, keywords, head)
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
        return True

    def remove_key(self, key):
        """ Removes key and associate list from topDict """
        del self.topDict[key]
        return True

    def clean_key(self, key):
        """
        Clears the list associated with a key in the topDict
        Same funcitonality as clip_key(key, 0).
        """
        self.topDict[key] = []
        return True

    def clip_key(self, key, n):
        """ Clips list mapped by key to n elements """
        self.topDict[key] = self.topDict[key][:n]
        return True

    def insert_value(self, key, value):
        """ Adds value to the list mapped by key in topDict """
        self.topDict[key].append(value)
        return True

    def remove_value(self, key, domainReverse):
        """
        Removes elemetnt with given domainReverse from list
        mapped by key in topDict
        """
        domainEqual = lambda elt : (elt[1] != domainReverse)
        self.topDict[key] = list(filter(domainEqual, self.topDict[key]))
        return True

    def sort_key(self, key, index=1):
        """
        Sorts key based on index of elts.
        Default index is 0, aka pageRank score
        """
        indexLambda = lambda elt : elt[index]
        self.topDict[key].sort(key=indexLambda)
        return True

    def sort_all(self, index=0):
        """ Sorts list mapped by each key in topDict based on index """
        indexLambda = lambda elt : elt[index]
        for key in self.topDict:
            self.topDict[key].sort(key=indexLambda)
        return True

    def search_index(self, key, indexLambda, n=20):
        """
        Returns the data at indexLambda of the top n elements of the list mapped
        by key in topDict
        """
        return list(map(indexLambda, self.topDict[key][:n]))

    def search_full(self, key, n=20):
        """ Returns the top n elements of the list mapped by key in topDict """
        return self.topDict[key][:n]

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
#

x = Thicctable(keys=['a','b','c'])

x.insert_value('b', ('hi', 1))

x.insert_value('b', ('hey', 3))

x.insert_value('b', ('yo', 2))

x.insert_value('a', ('a', 2))

x.insert_value('a', ('b', 1))

x.sort_all(1)

print(x.search_index('a', (lambda x: x[0])))

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
