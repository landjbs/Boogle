import searchers.databaseSearcher as databaseSearcher
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import find_rawTokens

def topSearch(rawSearch, database, knowledgeProcessor):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
    CURRENTLY: Uses databaseSearcher.single_search if search contains
    one knowledge token, else uses databaseSearcher.and_search
    """
    cleanedSearch = clean_text(rawSearch)
    tokenList = find_rawTokens(cleanedSearch, knowledgeProcessor)
    if (len(tokenList) == 1):
        return databaseSearcher.single_search(tokenList[0], database)
    else:
        return databaseSearcher.and_search(tokenList, databases)
