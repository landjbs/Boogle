"""
Functions for all text processing involding knowledgeSet and knowledgeProcessor
built in models.knowledge.knowledgeBuilder.
"""

import re
import math
import models.knowledge.knowledgeBuilder as knowledgeBuilder
import numpy as np
import matplotlib.pyplot as plt

# dict mapping html divs to score  multiplier
divScores = {'title':6, 'h1':5, 'h2':4, 'h3':3, 'lowHeaders':2, 'description':3, 'keywords':3, 'imageAlt':2, 'all':1}


def find_rawTokens(inStr, knowledgeProcessor):
    """
    Finds set of tokens used in inStr without scoring or count.
    Used to tokenize search queries.
    Looks for both full tokens from knowledgeSet and single-word (sub) tokens
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
    tokensFound = set(find_rawTokens(divText, knowledgeProcessor))


    def score_token(token i):
        """
        Helper to score individual token in current div
        """
        # find number of occurences of a token in divText
        tokenNum = knowledgeBuilder.count_token(token, divText)

    def score_token(token, i):
        """
        Helper to score token as function of frequency in current text relative
        to average frequency and multiplier associated with page div
        """
        # find number of occurences of a token in divText
        tokenNum = knowledgeBuilder.count_token(token, divText)
        # find frequency of token usage in divText
        tokenFrequency = (tokenNum / divLen)

        ### DIV SPECIFIC SCORING ###
        # if div is all, score the token based on how close it is to the start and benefit longer pages
        if (div=='all'):
            ########################
            # find start and end location of each token usage in the text
            tokenLocs = [(loc.span()[0], loc.span()[1]) for loc in re.finditer(token, divText, flags=re.IGNORECASE)]
            # get loc of first token usage
            firstUse = tokenLocs[0]
            # spacing
            ########################
            # get page length relative to average word count (assumed 700)
            relativeLength = divLen / 700
            # use sigmoid function on relative length to benefit longer pages with equal token freq to shorter (multiplier asymptotes at 1 and ~5)
            lengthMultiplier = (math.exp(0.25 * relativeLength) / (math.exp(0.25 * (relativeLength - 5.2)) + 1)) + 1
            tokenFrequency *= lengthMultiplier

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
    scoreDict = {token:score_token(token, i) for i, token in enumerate(tokensFound)}
    # filter scores below cuoff
    filteredScores = {token: score for token, score in scoreDict.items() if score > cutoff}
    return filteredScores


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
        divScores = find_scoredTokens(divText, div, knowledgeProcessor, freqDict, 0.05)
        # iterate over found tokens, adding their scores to the divDict
        for token in divScores:
            if token in scoreDict:
                scoreDict[token] += divScores[token]
            else:
                scoreDict.update({token:divScores[token]})
    return scoreDict








pass
