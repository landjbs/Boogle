"""
Functions for all text processing involding knowledgeSet and knowledgeProcessor
built in models.knowledge.knowledgeBuilder.
"""

import re
import models.knowledge.knowledgeBuilder as knowledgeBuilder


# dict mapping html divs to score  multiplier
divScores = {'title':20, 'headers':5, 'description':18, 'keywords':19, 'all':1}


def find_rawTokens(inStr, knowledgeProcessor):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    Looks for both full tokens from knowledgeSet and single-word tokens
    """
    # use greedy matching of flashtext algorithm to find keywords
    greedyTokens = list(knowledgeProcessor.extract_keywords(inStr))
    # initialize list of all tokens with greedy tokens
    allTokens = greedyTokens.copy()
    # iterate over greedy tokens
    for token in greedyTokens:
        splitToken = token.split()
        if not (len(splitToken)==1):
            # iterate over white-space delimited words in each token
            for word in token.split():
                # find all tokens within the word and add to all tokens
                smallTokens = knowledgeProcessor.extract_keywords(word)
                allTokens += smallTokens
    return allTokens


def find_countedTokens(inStr, knowledgeProcessor):
    """
    Finds dict mapping tokens used in inStr to number of times used.
    Does not normalize by length, div, or average frequency.
    """
    tokensFound = find_rawTokens(inStr)
    return {token:knowledgeBuilder.count_token(token, inStr) for token in tokensFound}


def find_scoredTokens(divText, div, knowledgeProcessor, freqDict, cutoff):
    """
    Args: Text of division being analyzed, name of division, processor to find
    tokens, dict of average word frequencies, score cutoff to include token in
    dict.
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
        tokenNum = knowledgeBuilder.count_token(token, divText)
        # find frequency of token usage in divText
        tokenFrequency = tokenNum / divLen
        # find average frequency of token from freqDict; if no key in freqDict, avgFreq <- 0
        try:
            avgFreq = freqDict[token]
        except:
            avgFreq = 0
        # normalize observed frequency by subtracting average frequency
        normFreq = tokenFrequency - avgFreq
        # if normalized frequency is less than or equal to zero, score is zero
        if normFreq <= 0:
            score = 0
        else:
            # find the multiplier for the page div from divScores, 0 if not specified
            try:
                divMultipier = divScores[div]
            except:
                divMultipier = 1
            # token score is normalized frequency times div multiplier
            score = (normFreq ** (1/3)) * divMultipier
        return score

    # apply analyze_token to create dict mapping tokens to scores
    scoreDict = {token:score_token(token) for token in tokensFound if score_token(token)>cutoff}
    return scoreDict


def score_divDict(divDict, knowledgeProcessor, freqDict):
    """
    Args: Dict mapping page divisions to cleaned content (eg. {'title':'foo',
    'p':'hello world'}), knowledgeProcessor to use for matching, and dict of
    average knowledge token frequency.
    Returns: Dict mapping all knowledge tokens found in divDict to score
    determined by div found and relative frequency.
    """
    # initialize dict to hold tokens mapping to sum scores across all divs
    scoreDict = {}
    # iterate over divisions in divDict
    for div in divDict:
        # get text inside div
        divText = divDict[div]
        # get dict of tokens in divText and their scores
        divScores = find_scoredTokens(divText, div, knowledgeProcessor, freqDict, 0.001)
        # iterate over found tokens, adding their scores to the divDict
        for token in divScores:
            if token in scoreDict:
                scoreDict[token] += divScores[token]
            else:
                scoreDict.update({token:divScores[token]})
    return scoreDict








pass
