"""
Parses a raw search string and employs a search algorithm from
searchers.databaseSearcher depending on lexical understanding of the query
"""

# load crawl materials first
from dataStructures.objectSaver import load
from crawlers.crawlLoader import load_crawled_pages
database, uniqueWords, searchProcessor = load_crawled_pages('backend/data/thicctable/wikiCrawl_NOVECS')
freqDict = load('backend/data/outData/knowledge/freqDict.sav')
# delete loading functions to free up a little space
for o in dir():
    if not o in ['__annotations__', '__builtins__', '__cached__', '__doc__',
                '__file__', '__loader__', '__name__', '__package__', '__spec__',
                '__warningregistry__', 'database', 'uniqueWords',
                'searchProcessor', 'freqDict']:
        del o

# external imports
import re
from time import time
from keras.models import load_model

# data structures
from dataStructures.resultObj import ResultObject
# models
from models.processing.cleaner import clean_search
from models.knowledge.knowledgeFinder import find_rawTokens
# searching
from searchers.spellingCorrector import correct
import searchers.databaseSearcher as databaseSearcher
from searchers.querySentiment import score_token_importance


n = 10

# paraModel = load_model('backend/data/outData/searchAnalysis/paragraphAnswering2.sav')

def topSearch(rawSearch, user):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
        -rawSearch:     Unedited string of the search
        -user:          IP of the user who initiated the search
    """
    timeStart = time()

    ### QUERY PROCESSING ###
    cleanedSearch = clean_search(rawSearch)
    correctedSearch = " ".join([correct(token, uniqueWords) if not (token.startswith('"') and token.endswith('"')) else token[1:-1]
                                for token in cleanedSearch.split()])
    correctionDisplay = None if (cleanedSearch==correctedSearch) else (correctedSearch, cleanedSearch)
    # find greedy tokens only for the first search
    tokenSet = set(searchProcessor.extract_keywords(correctedSearch))

    ### SEARCHING ###
    numResults, resultList = 0, []
    # single token protocol
    if (len(tokenSet) == 1):
        print('TOP: SINGLE')
        topToken = list(tokenSet)[0]
        # query database for single token bucket. error means it's empty
        try:
            singleResults = databaseSearcher.single_search(topToken, database)
            numResults += singleResults[0]
            resultList += singleResults[1]
        except:
            pass
        if numResults < n:
            print(f'AND After {numResults}')
            words = topToken.split()
            numWords = len(words)
            if (numWords > 1):
                tokenSet.update(find_rawTokens(cleanedSearch, searchProcessor))
                tokenScores, searchVec, queryType = score_token_importance(cleanedSearch, words, freqDict)
                andResults = databaseSearcher.weighted_and_search(tokenScores, database, (n-numResults))
                # andResults = databaseSearcher.weighted_vector_search(tokenScores, database, searchVec, n)
                numResults += andResults[0]

                # add all results from andResult if they aren't already there
                for andResult in andResults[1]:
                    if not andResult in resultList:
                        resultList.append(andResult)
            else:
                pass

    # multi token protocol
    elif (len(tokenSet) > 1):
        print('TOP: AND')
        # score the importance of each token and perform intersectional weighted search
        tokenScores, searchVec, queryType = score_token_importance(cleanedSearch, tokenSet, freqDict)
        # andResults = databaseSearcher.weighted_vector_search(tokenScores, searchVec, database, n)
        andResults = databaseSearcher.weighted_and_search(tokenScores, database, n)

        # update search metrics
        numResults += andResults[0]
        resultList += andResults[1]

    else:
        print(f"WARNING: No tokens found in search {cleanedSearch}")

    # determine if an inverted result should be shown
    invertedResult = None
    for i, page in enumerate(resultList[:5]):
        if ((correctedSearch) in (page.title.lower()).strip()):
            invertedResult = resultList.pop(i).display_inverted(tokenSet)

    # get display obejcts of each page in resultList
    displayResultList = [pageObj.display(tokenSet) for pageObj in resultList]

    # calculate length of search time
    runTime = round((time() - timeStart), 4)

    # built result object to pass to app
    resultObj = ResultObject(rawSearch=rawSearch, runTime=runTime,
                            numResults=numResults, correction=correctionDisplay,
                            invertedResult=invertedResult, questionAnswer=None,
                            resultList=displayResultList, searchTime=timeStart,
                            user=user)

    return resultObj
