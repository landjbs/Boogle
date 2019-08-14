import json
import numpy as np
import matplotlib.pyplot as plt

from models.ranking.sortScorer import sort_score
from dataStructures.objectSaver import save, load
from dataStructures.postingObj import Posting


class Thicctable():
    """ Class to store indexed Page()s as keys mapping to Posting() objects """

    def __init__(self, keys):
        """
        Initialize branch as key-val store mapping keys to Posting()s
            -corrDict:  Dictionary mapping ALL tokens to a list of relatedTokens.
                            If there are no relatedTokens found, maps to empty list.
        """
        self.invertedIndex = {key:Posting(relatedTokens)
                                for key, relatedTokens in keys.items()}
        print(f"Table initialized with {len(keys)} buckets.")

    ### FUNCTIONS FOR MODIFYING KEYS ###
    def add_key(self, key):
        """ Adds key and corresponding empty list to invertedIndex """
        self.invertedIndex.update({key:Posting()})
        return True

    def remove_key(self, key):
        """ Removes key and associated list from invertedIndex """
        del self.invertedIndex[key]
        return True

    def kill_smalls(self, n):
        """ Removes keys with lists under length n. Use carefully! """
        # find keys that map to a list shorter than n
        smallKeys = [key for key, posting in self.invertedIndex.items()
                        if  posting.len_posting() < n]
        for key in smallKeys:
            del self.invertedIndex[key]
        return True

    def kill_empties(self):
        """ Faster version of kill_smalls(n=1) to kill empty keys """
        emptyKeys = [key for key, posting in self.invertedIndex.items()
                        if posting.is_empty()]
        print(f'Num Empty: {len(emptyKeys)}')
        for key in emptyKeys:
            del self.invertedIndex[key]
        return True

    ### FUNCTIONS FOR MODIFYING KEY-MAPPED POSTINGS LISTS ###
    def clear_key(self, key):
        """
        Clears the list associated with a key in the invertedIndex
        Same funcitonality as clip_key(key, 0).
        """
        self.invertedIndex[key] = Posting()
        return True

    def clip_key(self, key, n):
        """ Clips list mapped by key to n elements """
        self.invertedIndex[key].clip_postingList(n)
        return True

    def insert_pageTuple(self, key, pageTuple):
        """ Adds value to the potsingList mapped by key in invertedIndex """
        self.invertedIndex[key].add_to_postingList(pageTuple)
        return True

    def remove_value(self, key, url):
        """
        Removes elements with given url from list mapped by key in invertedIndex
        """
        self.invertedIndex[key].remove_from_postingList(url)
        return True

    def sort_key(self, key):
        """ Sorts key list based on page scores (first elt of tuple) """
        self.invertedIndex[key].sort_postingList()
        return True

    def sort_all(self):
        """ Sorts list mapped by each key in invertedIndex based on index """
        for key in self.invertedIndex:
            self.sort_key(key)
        return True

    def bucket_page(self, pageObj):
        """
        Args: Page object to insert into relevent buckets and score.
        Wraps insert_value and calls models.ranking to score page and sort
        into all applicable buckets
        """
        # pull tokens from pageObj
        pageTokens = pageObj.knowledgeTokens
        for token in pageTokens:
            try:
                # get score of page from pageRanker
                pageScore = sort_score(pageObj, token)
                # create bucket-specific pageTuple of score and pageObj
                pageTuple = (pageScore, pageObj)
                # insert tuple of score and pageObj into appropriate bin
                self.insert_pageTuple(key=token, pageTuple=pageTuple)
            except KeyError as key:
                print(f"BUCKETING ERROR: {key}")
                # if token isn't in index yet, add it and re-call function
                self.add_key(token)
                self.bucket_page(pageObj)
            except Exception as e:
                print(e)
        return True

    ### FUNCTIONS FOR MODIFYING KEY-MAPPED SEARCH COUNTS AND RELEVANCES ###
    def initialize_relevances(self):
        """ Initializes relevance computation across every key in the table """
        for posting in self.invertedIndex.values():
            posting.calc_relevance()
        return True

    ### SEARCH FUNCTIONS ###
    def search_display(self, key, tokenList, n):
        """
        Returns display tuple from top n pages from (sorted) key with
        window text according to token list
        """
        return self.invertedIndex[key].search_display_topPostings(tokenList, n)

    def search_pageObj(self, key, n):
        """
        Returns list of page objects in key, discarding scores.
        Useful if pages need to be reranked (eg. and_search).
        """
        return self.invertedIndex[key].search_pageObj_topPostings(n)

    def search_full(self, key, n):
        """ Returns the top n pageTuples of the list mapped by key in invertedIndex """
        return self.invertedIndex[key].search_full_topPostings(n)

    def search_relatedTokens(self, key, n):
        """ Gets related tokens for a key """
        return self.invertedIndex[key].relatedTokens[:n]

    ### SAVE/LOAD FUNCTIONS ###
    def save(self, outPath):
        """ Writes contents of Thicctable to json file in outPath.json """
        with open(f"{outPath}.json", 'w+') as FileObj:
            json.dump(self.invertedIndex, FileObj)
        return True

    def load(self, inPath):
        """ Loads invertedIndex saved in json file """
        with open(f"{inPath}.json", 'r') as FileObj:
            self.invertedIndex = json.load(FileObj)
        return True

    ### METRICS FUNCTIONS ###
    def key_length(self, key):
        """
        Returns the length of the value list associated with a key.
        Useful metric for comparing importance of keys.
        """
        return self.invertedIndex[key].len_posting()

    def all_lengths(self):
        """ Get length of posting list for each singe-word token in invertedIndex """
        return {key:(posting.len_posting())
                for key, posting in self.invertedIndex.items()
                if not ((len(key.split())==1) and not (posting.is_empty()))}

    def all_relevances(self):
        """
        Returns dict mapping each token in the table to its relevance.
        INITIALIZATION MUST BE COMPLETED FIRST AND SEPARATELY """
        return {key:(posting.relevance)
                for key, posting in self.invertedIndex.items()}

    def plot_lengths(self, outPath=""):
        """
        Plot bar chart of lengths of value lists associated with invertedIndex
        keys and print length metrics across all lists.
        """
        # get list of all keys and list of length of values
        keyList, lengthList = self.invertedIndex.keys(), list(map(lambda posting : posting.len_posting(), self.invertedIndex.values()))
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

    def plot_key_metrics(self, key, indexLambda, outPath=""):
        """
        Print and plot metrics for data accessed  by index lambda across
        elements of list mapped by key. Only works for number values,
        such as score, length, time, etc.
        """
        # fetch list mapped by key
        valueList = self.invertedIndex[key].postingList
        # apply indexLambda to get data of interest
        mappedList = list(map(indexLambda, valueList))
        # get metrics of mappedList
        mappedMean = np.mean(mappedList)
        mappedMin, mappedMax = min(mappedList), max(mappedList)
        print(f"Metrics:\n\tMean: {mappedMean}\n\tMin: {mappedMin}\n\tMax: {mappedMax}")
        # plot mappedList from head to tail
        plt.plot(mappedList)
        plt.title(f"Indexed Metrics of {key} Key")
        plt.xlabel("Index in List")
        plt.ylabel("Value")
        if not (outPath==""):
            plt.savefig(outPath)
        else:
            plt.show()
        return True
