"""
Functions for all text processing involding knowledgeSet and knowledgeProcessor
built in models.knowledge.knowledgeBuilder.
"""

import re
from flashtext import KeywordProcessor

knowledgeProcessor = KeywordProcessor(case_sensitive=False)
knowledgeProcessor.add_keyword('foo')
knowledgeProcessor.add_keyword('bar')

# dict mapping html divs to score  multiplier
divScores = {'title':20, 'h1':5, 'p':1}

# keywordDict = {keyword:(len(re.findall(keyword, pageText, re.IGNORECASE))) for keyword in keywordsFound}

def find_rawTokens(inStr, knowledgeProcessor):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    """
    return set(knowledgeProcessor.extract_keywords(inStr))

def score_token(token, freq, div):
    """
    Args: single knowledge token and html division where it occurred
    Returns: score of token weighted by
    """
    divMultipier = divScores[div]
    score = freq * divMultipier
    return score


def find_weightedTokens(divText, div, knowledgeProcessor):
    """
    Returns dict mapping knowledge tokens to score assigned by score_token
    """
    # find number of words in divText
    divLen = len(divText.split())
    # use knowledgeProcessor to extract tokens from page text
    tokensFound = set(knowledgeProcessor.extract_keywords(divText))
    # iterate over the tokens found
    for token in tokensFound:
        # find number of occurences of a token in divText
        tokenNum = len(re.findall(token, divText, flags=re.IGNORECASE))
        # find frequency of token usage in divText
        tokenFrequency = tokenNum / divLen
        # score token based on token, frequency, and div
        tokenScore = score_token(token, tokenFrequency, div)
        print(f"{token}: {tokenScore}")


def find_weighted_knowledge(divDict):
    """
    Args:
        divDict- Dict generated by crawlers.htmlAnalyzer mapping from
                 html divisions to the string of their contents.

    Returns: Single dict mapping from knowledgeTokens found to score assigned
    by weight

    Sample input: {'title':'foo bar', 'h1':'foo', 'p':'hello world'}
    """
    for div in divDict:
        divText = divDict[div]
        weightedTokens = find_weightedTokens(divText, div, knowledgeProcessor)

        # tokenDict = (find_tokens(divDict[div], knowledgeProcessor))
        # tokenDict = dict(map(lambda k : (k[0], k[1]/2), tokenDict.items()))
        # print(tokenDict)



find_weighted_knowledge({'title':'foo foo foo bar', 'h1':'foo', 'p':'hello world'})










pass