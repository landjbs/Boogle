# Converts searchString into weighted list of search tokens
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import find_rawTokens

def get_search_tokens(rawSearch, knowledgeProcessor):
    """
    Finds knowledge tokens of any size in searchString.
    """
    cleanSearch = clean_text(rawSearch)
    searchTokens = find_rawTokens(cleanSearch, knowledgeProcessor)
    return searchTokens
