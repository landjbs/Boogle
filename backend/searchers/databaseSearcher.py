"""
Database searcher provides several methods for searching a Thicctable database
for lists of results.
"""

from numpy import sum
from itertools import chain
from operator import itemgetter

from models.binning.docVecs import vectorize_doc
from models.ranking.intersectionalRanker import (score_token_intersection,
                                                score_vector_intersection)


### Simple search algorithms ###
def single_search(token, database, n):
    """
    Performs a a databases search for a single token and returns the display
    attributes of the top n items.
    Fastest type of search: no intersection and no re-ranking.
    """
    resultList = database.search_pageObj(key=token, n=n)
    numResults = database.key_length(key=token)
    return (numResults, resultList)


def and_search(tokenList, database, n):
    """
    Preforms an AND search for the intersection multiple search tokens.
    Slower than single_search or or_search as pages need to be reranked.
    """
    # get list of all result buckets associate with each tokens in token list
    bucketList = [database.search_pageObj(key=token, n=100000)
                    for token in tokenList]
    # get list of length of each token's bucket
    lengthList = [database.key_length(key=token) for token in tokenList]
    # pop shortest bucket from bucketList and cast as set
    shortestBucket = set(bucketList.pop(lengthList.index(min(lengthList))))
    # concatenate all buckets but the shortest
    otherBuckets = list(chain.from_iterable(bucketList))
    # cast shortestBucket to a set and get its interesction with otherBuckets
    intersectionPages = shortestBucket.intersection(otherBuckets)
    # rank intersection pages according to all tokens
    rankedPages = [(score_simple_intersection(pageObj, tokenList), pageObj)
                    for pageObj in intersectionPages]
    rankedPages.sort(reverse=True, key=itemgetter(0))
    # find number of pages before filtering down to n
    numResults = len(rankedPages)
    # return top n pages and disregard their scores
    resultList = [pageElt[1] for pageElt in rankedPages[:n]]
    return (numResults, resultList)


def or_search(tokenList, database, n):
    """
    Performs an OR search accross a list of tokens.
    Ranks based on original score, since no intersectional re-ranking is
    necessary.
    NB: The presence of multiple tokens from tokenList in a page does not
    influence it's ranking.
    """
    # get list of all result buckets associate with each tokens in token list
    bucketLists = [database.search_full(key=token, n=100000)
                    for token in tokenList]
    # combine bucketLists into a single, sorted list
    sortedResults = list(chain.from_iterable(bucketLists))
    sortedResults.sort(reverse=True, key=itemgetter(0))
    resultList = [pageElt[1].display(tokenList)
                    for i, pageElt in enumerate(sortedResults) if i < n]
    return resultList


### Weight Search Algorithms ###
def weighted_and_search(tokenScores, database, n):
    """
    Performs AND search for intersection of multiple tokens where tokens are
    each given ranking of importance in the search
    """
    # find the most important token and retrive its bucket
    importantToken = max(tokenScores, key=(lambda elt:tokenScores[elt]))
    importantBucket = set(database.search_pageObj(key=importantToken, n=100000))
    # get the buckets of the less important tokens in the search
    otherTokens = tokenScores.copy()
    _ = otherTokens.pop(importantToken)
    bucketList = [database.search_pageObj(key=token, n=100000)
                    for token in otherTokens]
    otherBuckets = list(chain.from_iterable(bucketList))
    # find those pages in that of the most important token and any of the others
    intersectionPages = importantBucket.intersection(otherBuckets)
    # rank the pages according to their tokens and sort by ranking
    rankedPages = [(score_token_intersection(pageObj, tokenScores), pageObj)
                    for pageObj in intersectionPages]
    rankedPages.sort(reverse=True, key=itemgetter(0))
    # find number of pages before filtering to n
    numResults = len(rankedPages)
    # return top n pages and disregard their scores
    resultList = [pageElt[1] for pageElt in rankedPages[:n]]
    return (numResults, resultList)


def weighted_and_search(tokenSscores, database, n):
    """ Searches database using new algorithm """
    bucketList = [database.search_pageObj(key=token, n=100000)
                    for token in tokenScores]
    for bucketList 


def _weighted_and_search(tokenScores, database, n):
    bucketList = [database.search_full(key=token, n=100000)
                    for token in tokenScores]
    # get number of pages avaliable to return
    avaliableResults = 0
    for bucket in bucketList:
        avaliableResults += len(bucket)
    # actual number of results to find
    resultNum = min(n, avaliableResults)
    # list to hold ~sorted Page() objects of results
    resultList = []
    # iterate over number of results to show
    for i in range(resultNum):
        topList = []
        for index, bucket in enumerate(bucketList):
            try:
                pageObject = bucket[0][1]
                pageScore = score_token_intersection(pageObject, tokenScores)
                topList.append((pageScore, index))
            except:
                pass
        if topList == []:
            return (len(resultList), resultList)
        maxLoc = max(topList)[1]
        nextAddition = (bucketList[maxLoc].pop(0))[1]
        resultList.append(nextAddition)
    return (resultNum, resultList)


def weighted_or_search(tokenScores, database, n):
    """
    The same as weighted_and_search, but pages do not need to be a max
    importance bucket to qualify for ranking
    """
    bucketList = [database.search_pageObj(key=token, n=100000)
                    for token in tokenScores]
    allPages = list(chain.from_iterable(bucketList))
    rankedPages = [(score_simple_intersection(pageObj, tokenScores), pageObj)
                    for pageObj in allPages]
    rankedPages.sort(reverse=True, key=itemgetter(0))
    resultList = [pageElt[1].display(tokenScores.keys())
                    for i, pageElt in enumerate(rankedPages) if i < n]
    return resultList


def weighted_vector_search(tokenScores, searchVec, database, n):
    """ Weighted and search that uses ML on vector """
    # find the most important token and retrive its bucket
    importantToken = max(tokenScores, key=(lambda elt:tokenScores[elt]))
    importantBucket = set(database.search_pageObj(key=importantToken, n=100000))
    # get the buckets of the less important tokens in the search
    otherTokens = tokenScores.copy()
    _ = otherTokens.pop(importantToken)
    bucketList = [database.search_pageObj(key=token, n=100000)
                    for token in otherTokens]
    otherBuckets = list(chain.from_iterable(bucketList))
    # find those pages in that of the most important token and any of the others
    intersectionPages = importantBucket.intersection(otherBuckets)
    # rank the pages according to their tokens and sort by ranking
    rankedPages = [(score_vector_intersection(pageObj, tokenScores, searchVec),
                                                pageObj)
                    for pageObj in intersectionPages]
    rankedPages.sort(reverse=True, key=itemgetter(0))
    # find number of pages before filtering to n
    numResults = len(rankedPages)
    # return top n pages and disregard their scores
    resultList = [pageElt[1] for pageElt in rankedPages[:n]]
    return (numResults, resultList)
