import searchers.databaseSearcher as databaseSearcher
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import find_rawTokens
from searchers.spellingCorrector import correction

def topSearch(rawSearch, database, knowledgeProcessor):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
    CURRENTLY: Uses databaseSearcher.single_search if search contains
    one knowledge token, else uses databaseSearcher.and_search
    """
    cleanedSearch = clean_text(rawSearch)
    correctedSearch = " ".join([correction(token) for token in cleanedSearch.split()])
    #
    correctionDisplay = correctedSearch if not (cleanedSearch==correctedSearch) else None
    tokenList = find_rawTokens(correctedSearch, knowledgeProcessor)
    if (len(tokenList) == 1):
        return (correctionDisplay, databaseSearcher.single_search(tokenList[0], database))
    else:
        return (correctionDisplay, databaseSearcher.and_search(tokenList, database))
