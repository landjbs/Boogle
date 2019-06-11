import re
from flashtext import KeywordProcessor

def find_knowledgeTokens(pageText, knowledgeProcessor):
    """
    Returns dict mapping knowledge tokens found in text to number of occurences
    """
    # use knowledgeProcessor to extract tokens from page text
    keywordsFound = knowledgeProcessor.extract_keywords(pageText)
    # create dict mapping keywords to number of times used in pageText using re.findall()
    keywordDict = {keyword:(len(re.findall(keyword, pageText, re.IGNORECASE))) for keyword in keywordsFound}
    return keywordDict
