import searchers.databaseSearcher as databaseSearcher
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import find_rawTokens
from searchers.spellingCorrector import correction
from dataStructures.objectSaver import load
import re

from models.knowledge.knowledgeBuilder import build_knowledgeProcessor

# load knowledgeProcessor for finding tokens in search
print('Loading Knowledge Processor')
# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
knowledgeProcessor = build_knowledgeProcessor({'largest', 'wooden', 'sculpture'})
print("Processor loaded")
# lexicalParser = re.compile("AND|OR")
#

def topSearch(rawSearch, database):
    """
    Highest level search analyzer that takes in a raw search and decides
    which search function to employ.
    CURRENTLY: Uses databaseSearcher.single_search if search contains
    one knowledge token, else uses databaseSearcher.and_search
    """
    cleanedSearch = clean_text(rawSearch)

    cleanedSearch = re.sub('statue', 'sculpture', cleanedSearch)

    correctedSearch = " ".join([correction(token) if not (token[0]=='"' and token[-1]=='"') else token
                                for token in cleanedSearch.split()])

    correctionDisplay = correctedSearch
    # correctionDisplay = None if (cleanedSearch==correctedSearch) else correctedSearch

    tokenList = find_rawTokens(correctedSearch, knowledgeProcessor)
    print(tokenList)
    if (len(tokenList) == 1):
        return (correctionDisplay, databaseSearcher.single_search(tokenList[0], database))
    elif (len(tokenList)>1):
        return (correctionDisplay, databaseSearcher.and_search(tokenList, database))
