"""
Parses a raw search string and employs a search algorithm from
searchers.databaseSearcher depending on lexical understanding of the query
"""

import re
import numpy as np

import searchers.databaseSearcher as databaseSearcher
from searchers.querySentiment import score_token_importance
from searchers.spellingCorrector import correct
from models.processing.cleaner import clean_search
from models.knowledge.knowledgeFinder import find_rawTokens

from keras.models import load_model
from models.binning.docVecs import vectorize_doc

paraModel = load_model('data/outData/searchAnalysis/paragraphAnswering2.sav')

def topSearch(rawSearch, database, uniqueWords, knowledgeProcessor, freqDict):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
    """
    ### QUERY PROCESSING ###
    n = 20
    cleanedSearch = clean_search(rawSearch)
    correctedSearch = " ".join([correct(token, uniqueWords) if not (token.startswith('"') and token.endswith('"')) else token[1:-1]
                                for token in cleanedSearch.split()])
    correctionDisplay = None if (cleanedSearch==correctedSearch) else (correctedSearch, cleanedSearch)
    # find greedy tokens only for the first search
    tokenSet = set(knowledgeProcessor.extract_keywords(correctedSearch))

    ### SEARCHING ###
    numResults, resultList = 0, []
    # protocol for single token at top level of search
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
                tokenSet.update(find_rawTokens(cleanedSearch, knowledgeProcessor))
                tokenScores, searchVec, queryType = score_token_importance(cleanedSearch, words, freqDict)
                # andResults = databaseSearcher.weighted_and_search(tokenScores, database, (n-numResults))
                andResults = databaseSearcher.weighted_vector_search(tokenScores, database, searchVec, n)
                numResults += andResults[0]

                if queryType=="question":
                    print('Type: question')
                    topPage = andResults[0]
                    topText = topPage.windowText
                    halfChar = len(topWords) / 2
                    paraList = [topText[:halfChar], topText[halfChar:]]
                    for para in paraList:
                        paraVec = vectorize_doc(para)
                        distVec = np.subtract(searchVec, paraVec)


                # add all results from andResult if they aren't already there
                for andResult in andResults[1]:
                    if not andResult in resultList:
                        resultList.append(andResult)
            else:
                pass

    # protocol for more than one token
    elif (len(tokenSet) > 1):
        print('TOP: AND')
        # score the importance of each token and perform intersectional weighted search
        tokenScores, searchVec = score_token_importance(cleanedSearch, tokenSet, freqDict)
        andResults = databaseSearcher.weighted_vector_search(tokenScores, searchVec, database, n)
        # update search metrics
        numResults += andResults[0]
        resultList += andResults[1]

    else:
        print(f"WARNING: No tokens found in search {cleanedSearch}")

    # determine if an inverted result should be shown
    invertedResult = None
    for i, page in enumerate(resultList[:5]):
        if (((page.title).lower().strip())==(correctedSearch)):
            invertedResult = resultList.pop(i).display_inverted(tokenSet)

    # get display obejcts of each page in resultList
    displayResultList = [pageObj.display(tokenSet) for pageObj in resultList]

    return (correctionDisplay, numResults, invertedResult, displayResultList)
