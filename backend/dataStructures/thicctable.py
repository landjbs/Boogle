from objectSaver import save, load
import matplotlib.pyplot as plt

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

    ### FUNCTIONS FOR MODIFYING KEYS ###
    def add_key(self, key):
        """ Adds key and corresponding empty list to topDict """
        self.topDict.update({key:[]})
        return True

    def remove_key(self, key):
        """ Removes key and associate list from topDict """
        del self.topDict[key]
        return True

    ### FUNCTIONS FOR MODIFYING KEY-MAPPED LISTS ###
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
        # create lambda to pull element for sorting
        indexLambda = lambda elt : elt[index]
        self.topDict[key].sort(key=indexLambda)
        return True

    def sort_all(self, index=0):
        """ Sorts list mapped by each key in topDict based on index """
        # create lambda to pull element for sorting
        indexLambda = lambda elt : elt[index]
        # iterate over keys and sort
        for key in self.topDict:
            self.topDict[key].sort(key=indexLambda)
        return True

    ### SEARCH FUNCTIONS ###
    def search_index(self, key, indexLambda, n=20):
        """
        Returns the data at index pulled by lambda of the top n elements of the
        list mapped by key in topDict
        """
        return list(map(indexLambda, self.topDict[key][:n]))

    def search_full(self, key, n=20):
        """ Returns the top n elements of the list mapped by key in topDict """
        return self.topDict[key][:n]

    ### DATA MODIFICATION FUNCTIONS ###
    def save(self, outPath):
        """ Saves object to outPath, wraps objectSaver.save() """
        save(self, outPath)

    ### VISUALIZATION FUNCTIONS ###
    def metrics_full(self):
        """ Display metrics for every key in topList """
        keyList, valueList = self.topDict.keys(), self.topDict.values()
        lengthList = list(map(lambda elt : len(elt), valueList))
        plt.bar(keys, values)
        # plt.title("Number of Pages Per Key")

        # plt.xticks(keyList)
        # plt.show()
        return True





# Testing

import time
import numpy as np

NUM = 10

x = Thicctable(keys=['a','b','c'])

keyList = np.random.choice(['a','b','c'], size=NUM)
v1List = np.random.randint(0, 10000, size=NUM)
v2List = np.random.choice(['a','b','c','d','e','f','g','c'], size=NUM)

insertStart = time.time()
for i, key in enumerate(keyList):
    x.insert_value(key, (v1List[i], v2List[i]))
insertEnd = time.time()
print(f"Insertion: {insertEnd - insertStart}")

sortStart = time.time()
x.sort_all(index=0)
sortEnd = time.time()
print(f"Sorting: {sortEnd - sortStart}")

start = time.time()
print(x.search_index('a', indexLambda=(lambda x:x[1])))
end  = time.time()
iSearch = end - start

start = time.time()
print(x.search_full('a'))
end  = time.time()
aSearch = end - start

print(f"Search:\n\ti:  {iSearch}\n\ta: {aSearch}")

x.metrics_full()

saveStart = time.time()
x.save("test.thicc")
saveEnd = time.time()
print(f"Save: {saveEnd - saveStart}")






pass
