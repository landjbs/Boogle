"""
Functions for all text processing involding knowledgeSet and knowledgeProcessor
built in models.knowledge.knowledgeBuilder.
"""

import re
from flashtext import KeywordProcessor

knowledgeProcessor = KeywordProcessor(case_sensitive=False)
knowledgeProcessor.add_keyword('foo')
knowledgeProcessor.add_keyword('bar')
knowledgeProcessor.add_keyword('hello')

# dict mapping html divs to score  multiplier
divScores = {'title':20, 'h1':5, 'p':1}
freqDict = {'foo':0.4, 'bar':0.01}


def find_rawTokens(inStr, knowledgeProcessor):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    """
    return set(knowledgeProcessor.extract_keywords(inStr))


def find_scoredTokens(divText, div, knowledgeProcessor, cutoff):
    """
    Args: Text of division being analyzed, name of division, processor to find
    tokens, score cutoff to include token in dict.
    Returns: Dict of tokens in divText mapping to score assigned by score_token
    """
    # find number of words in divText
    divLen = len(divText.split())
    # use knowledgeProcessor to extract tokens from page text
    tokensFound = set(knowledgeProcessor.extract_keywords(divText))

    def score_token(token):
        """
        Helper to score token as function of frequency in current text relative
        to average frequency and multiplier associated with page div
        """
        # find number of occurences of a token in divText
        tokenNum = len(re.findall(f"(?<![a-zA-Z]){token}(?![a-zA-Z])", divText, flags=re.IGNORECASE))
        # find frequency of token usage in divText
        tokenFrequency = tokenNum / divLen
        # find average frequency of token from freqDict; no key in freqDict, avgFreq <- 0
        try:
            avgFreq = freqDict[token]
        except:
            avgFreq = 0
        # normalize observed frequency by subtracting average frequency
        normFreq = tokenFrequency - avgFreq
        # if the normalized frequency is less than or equal to zero, score is zero
        if normFreq <= 0:
            score = 0
        else:
            # find the multiplier for the page div from divScores
            divMultipier = divScores[div]
            # token score is normalized frequency times div multiplier
            score = normFreq * divMultipier
        return score

    # apply analyze_token to create dict mapping tokens to scores
    scoresDict = {token:score_token(token) for token in tokensFound}
    return scoresDict





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
        print(div)
        weightedTokens = find_scoredTokens(divText, div, knowledgeProcessor, 0)

        # tokenDict = (find_tokens(divDict[div], knowledgeProcessor))
        # tokenDict = dict(map(lambda k : (k[0], k[1]/2), tokenDict.items()))
        # print(tokenDict)



find_weighted_knowledge({'title':'foo foo foo bar', 'h1':'foo', 'p':'hello world'})










pass
