"""
Functions for all text processing involding knowledgeSet and knowledgeProcessor
built in models.knowledge.knowledgeBuilder.
"""

import re
import math
from numpy import log
import matplotlib.pyplot as plt

# dict mapping html divs to score  multiplier
divMultipiers = {'url':5, 'title':6, 'h1':5, 'h2':4, 'h3':3, 'lowHeaders':2, 'description':3, 'keywords':3, 'imageAlt':2, 'all':1}


def count_token(token, pageText):
    """
    Uses regexp to return number of times a token is used in pageText.
    Matches for tokens that are not parts of larger, uninterrupted words.
    Does not require a knowledgeProcessor.
    """
    return len(re.findall(f"(?<![a-zA-Z]){token}(?![a-zA-Z])", pageText, flags=re.IGNORECASE))


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
    Subtokens should be given 3/4 the weighting of full tokens
    """
    tokensFound = find_rawTokens(inStr)
    return {token:count_token(token, inStr) for token in tokensFound}


def score_token(token, div, divLen, divMultipier, tokensFound):
    """
    Helper to score individual token in current div
    """
    ### FIND TOKEN FREQUENCY ###
    tokenNum = knowledgeBuilder.count_token(token, divText)
    tokenFreq = tokenNum / divLen

    ### NORMALIZE TOKEN FREQUENCY ###
    # get term and document frequency of token in freqDict built on scraped data
    try:
        termFreq, docFreq = freqDict[token]
    except:
        termFreq, docFreq = 0, 0

    # normalize tokenFreq using a tf-idf schema
    relativeFreq = tokenFreq / termFreq
    normedFreq = (1 + np.log(relativeFreq))

    # tokens with negative normedFreq will automatically have scores of 0
    if normedFreq <= 0:
        return 0

    # apply sublinear scaling normedFreq to reduce impact of token-spamming
    scaledFreq = 1 + np.log(normedFreq)

    ### APPLY DIV-SPECIFIC SCORING MODELS ###
    if (div=='all'):
        ### TOKEN DISTRIBUTION SCORING ###
        # find start and end location of each token usage in the text
        tokenLocs = [(loc.span()[0], loc.span()[1]) for loc in re.finditer(token, divText, flags=re.IGNORECASE)]
        # get loc of first token usage
        firstUse = tokenLocs[0]

        ### RELATIVE LENGTH SCORING ###
        # get page length relative to average word count (assumed 700)
        relativeLen = divLen / 700
        # use sigmoid function on relative length to benefit longer pages with equal token freq to shorter (multiplier asymptotes at 1 and ~5)
        lengthMultiplier = (math.exp(0.25 * relativeLen) / (math.exp(0.25 * (relativeLen - 5.2)) + 1)) + 1
        normedFreq *= lengthMultiplier

    ### DIV MULTIPLICATION
    # apply div multiplier to boost tokens in important divs
    score = normedFreq * divMultipier

    return score


def find_scoredTokens(divText, div, knowledgeProcessor, freqDict, cutoff):
"""
Args: Text of division being analyzed, name of division, processor to find
tokens, dict of average word frequencies, score cutoff to include token in
dict.
Returns: Dict of tokens in divText mapping to score assigned by score_token
"""
# find number of words in divText
divLen = len(divText.split())
# find multiplier related to div
divMultipier = divMultipiers[div]
# use knowledgeProcessor to extract tokens from divText
tokensFound = set(find_rawTokens(divText, knowledgeProcessor))

# apply analyze_token to create dict mapping tokens to scores
scoreDict = {token:score_token(token, div, divLen, divMultipier, tokensFound)
                for token in tokensFound}

# filter scores below cuoff
filteredScores = {token: score for token, score in scoreDict.items()
                    if score > cutoff}

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
