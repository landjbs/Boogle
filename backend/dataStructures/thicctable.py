from objectSaver import save, load
import matplotlib.pyplot as plt
import numpy as np

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
        """ Removes key and associated list from topDict """
        del self.topDict[key]
        return True

    def kill_smalls(self, n):
        """ Removes keys with lists under length n. Use carefully! """
        # find keys that map to a list shorter than n
        smallKeys = [key for key in self.topDict if len(self.topDict[key]) < n]
        for key in smallKeys:
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
        Removes element with given domainReverse from list
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
        return True

    ### VISUALIZATION FUNCTIONS ###
    def plot_lengths(self, outPath=""):
        """ Display metrics for every key in topList """
        # get list of all keys and list of all values
        keyList, valueList = self.topDict.keys(), self.topDict.values()
        # find lengths for each element of valueList
        lengthList = list(map(lambda elt : len(elt), valueList))
        # get metrics of lengthList
        meanLength = np.mean(lengthList)
        minLength, maxLength= min(lengthList), max(lengthList)
        print(f"Length Metrics:\n\tMean: {meanLength}\n\tMin: {minLength}\n\tMax: {maxLength}")
        # plot keyList against lengthLis
        plt.bar(keyList, lengthList)
        plt.title("Number of Pages Per Key")
        plt.xlabel("Keys")
        plt.ylabel("Number Pages")
        if not (outPath==""):
            plt.savefig(outPath)
        else:
            plt.show()
        return True

    def plot_key_metrics(self, key, outPath=""):
        """ Print and plot metrics"""




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

x.kill_smalls(4)
# x.remove_key('a')

x.plot_lengths()

saveStart = time.time()
x.save("test.thicc")
saveEnd = time.time()
print(f"Save: {saveEnd - saveStart}")






pass
