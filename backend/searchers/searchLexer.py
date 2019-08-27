"""
Parses a raw search string and employs a search algorithm from
searchers.databaseSearcher depending on lexical understanding of the query
"""

# load crawl materials first
from dataStructures.objectSaver import load
from crawlers.crawlLoader import load_crawled_pages

(
    database,
    uniqueWords,
    searchProcessor
) = load_crawled_pages('backend/data/thicctable/wikiCrawl_SHADOW_NOVECS',
                        n=1000000, loadProcessor=False)

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
from searchers.invertedSelector import selected_inverted


n = 15

# set upper boundaries on search lengths
MAX_WORD_COUNT = 15
MAX_CHAR_COUNT = 80

# bert-serving-start -model_dir /Users/landonsmith/Desktop/shortBert -num_worker=1 -max_seq_len=20
# paraModel = load_model('backend/data/outData/searchAnalysis/paragraphAnswering2.sav')


class SearchError(Exception):
    """ Class for errors during searching """
    pass


def topSearch(rawSearch, user):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
        -rawSearch:     Unedited string of the search
        -user:          User() object of the user who initiated the search
    """
    timeStart = time()

    # validate query in length range
    if ((len(rawSearch.split()) > MAX_WORD_COUNT)
        or (len(rawSearch) > MAX_CHAR_COUNT)):
        raise SearchError('Search exceeds length limits')

    ### QUERY PROCESSING ###
    cleanedSearch = clean_search(rawSearch)
    correctedSearch = " ".join([correct(token, uniqueWords)
                                if not (token.startswith('"')
                                        and token.endswith('"'))
                                else token[1:-1]
                                for token in cleanedSearch.split()])
    correctionDisplay = None if (cleanedSearch==correctedSearch) else correctedSearch
    # find greedy tokens only for the first search
    tokenSet = set(searchProcessor.extract_keywords(correctedSearch))

    ### SEARCHING ###
    numResults, resultList = 0, []
    # single token protocol
    if (len(tokenSet) == 1):
        print('TOP: SINGLE')
        topToken = list(tokenSet)[0]
        # query database for single token bucket
        try:
            singleResults = databaseSearcher.single_search(topToken, database, n)
            numResults += singleResults[0]
            resultList += singleResults[1]
        except Exception as e:
            print(f'ERROR: {e}')
        if numResults < n:
            print(f'AND After {numResults}')
            words = topToken.split()
            numWords = len(words)
            if (numWords > 1):
                tokenSet.update(find_rawTokens(cleanedSearch, searchProcessor))
                tokenScores, searchVec, queryType = score_token_importance(cleanedSearch, words, database, freqDict)
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
        tokenScores, searchVec, queryType = score_token_importance(cleanedSearch, tokenSet, database, freqDict)
        # andResults = databaseSearcher.weighted_vector_search(tokenScores, searchVec, database, n)
        andResults = databaseSearcher.weighted_and_search(tokenScores, database, n)

        # update search metrics
        numResults += andResults[0]
        resultList += andResults[1]

    else:
        raise SearchError(f'Your search {rawSearch} returned no results.')

    # determine if an inverted result should be shown
    invertedResult, resultList = selected_inverted(correctedSearch,
                                                    resultList,
                                                    n=5)

    # if invertedResult found, convert it to display and decrement numResults
    if invertedResult:
        invertedResult = invertedResult.display_inverted(tokenSet)
        numResults -= 1

    # convert result list into list of display tuples
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
