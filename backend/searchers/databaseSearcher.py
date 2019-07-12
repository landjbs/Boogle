"""
Database searcher provides several methods for searching a Thicctable database
for lists of results.
    Methods:
        single_search:
"""

from models.ranking.pageRanker import score_intersection
from itertools import chain

def single_search(token, database, n=20):
    """
    Performs a a databases search for a single token and returns the display
    attributes of the top n items.
    Fastest type of search: no intersection and no re-ranking.
    """
    print("SINGLE search")
    resultList = database.search_display(key=token, tokenList=[token], n=n)
    print(f"{len(database.topDict[token])} results found.")
    return resultList

def smart_single_search(token, database, n=20):
    """
    Performs a database search for a single token, but will look for similar
    words and buckets to reach n results
    """
    print("SMART SINGLE search")
    resultList = database.search_display(key=token, tokenList=[token], n=n)
    resultLength = len(resultList)
    if (resultLength < 20):
        words = token.split()
        if (len(words)>1):
            resultList += and_search(words, database, n=(20-resultLength))
    return resultList

def or_search(tokenList, database, n=20):
    """
    Performs an OR search accross a list of tokens.
    Ranks based on original score, since no intersectional re-ranking is
    necessary.
    NB: The presence of multiple tokens from tokenList in a page does not
    influence it's ranking.
    """
    print("OR search")
    # get list of all result bukcets associate with each tokens in the token list
    bucketLists = [database.search_full(key=token, n=100000) for token in tokenList]
    # combine bucketLists into a single, sorted list
    sortedResults = list(chain.from_iterable(bucketLists)).sort(key=(lambda result:result[-1]), reverse=True)
    print(sortedResults)
    print(f"{len(sortedResults)} results found.")
    resultList = [pageElt[0].display(tokenList) for i, pageElt in enumerate(sortedResults) if i < n]
    return resultList


def and_search(tokenList, database, n=20):
    """
    Preforms an AND search for the intersection multiple search tokens.
    Slower than single_search or or_search as pages need to be reranked.
    """
    print("AND Search")
    # get list of all result buckets associate with each tokens in the token list
    bucketList = [database.search_pageObj(key=token, n=100000) for token in tokenList]
    print(f"{len(bucketList)} buckets found.")
    # get list of length of each bucket in bucketList
    lengthList = [len(bucket) for bucket in bucketList]
    # pop shortest bucket from bucketList and cast as set
    shortestBucket = set(bucketList.pop(lengthList.index(min(lengthList))))
    # concatenate all buckets but the shortest
    otherBuckets = list(chain.from_iterable(bucketList))
    # cast shortestBucket to a set and get its interesction with otherBuckets
    intersectionPages = shortestBucket.intersection(otherBuckets)
    print(f"{len(intersectionPages)} pages found.")
    # rank intersection pages according to all tokens
    rankedPages = [(score_intersection(pageObj, tokenList), pageObj) for pageObj in intersectionPages]
    rankedPages.sort(reverse=True, key=(lambda elt: elt[0]))
    print('sorted')
    returnPages = [pageElt[1].display(tokenList) for i, pageElt in enumerate(rankedPages) if i < n]
    return returnPages
