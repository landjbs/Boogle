import searchers.databaseSearcher as databaseSearcher
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import find_rawTokens
from dataStructures.objectSaver import load
import re
from searchers.spellingCorrector import correct
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor


# load knowledgeProcessor for finding tokens in search
print('Loading Knowledge Processor')
knowledgeProcessor = load('backend/data/outData/knowledge/knowledgeProcessor.sav')
print("Processor loaded")


def topSearch(rawSearch, database, WORDS):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
    CURRENTLY: Uses databaseSearcher.single_search if search contains
    one knowledge token, else uses databaseSearcher.and_search
    """
    cleanedSearch = clean_text(rawSearch)

    correctedSearch = " ".join([correct(token, WORDS) if not (token[0]=='"' and token[-1]=='"') else token
                                for token in cleanedSearch.split()])

    correctionDisplay = correctedSearch
    # correctionDisplay = None if (cleanedSearch==correctedSearch) else correctedSearch

    # tokenList = find_rawTokens(correctedSearch, knowledgeProcessor)
    tokenList = knowledgeProcessor.extract_keywords(correctedSearch)

    # use single
    if (len(tokenList) == 1):
        return (correctionDisplay, databaseSearcher.single_search(tokenList[0], database))

    elif (len(tokenList)>1):
        return (correctionDisplay, databaseSearcher.and_search(tokenList, database))
