"""
Scripts to analyze the sentiment of a search query. Methods
include finding the importance of each token as well as removing
stop words, classifying the search desire, and determining
locational/temporal tokens
"""

from numpy import log
from math import exp
from collections import Counter
# from models.binning.tokenScoring import get_masked_weights

# TO DO::: HAND TUNE SIGMOID ACT[pIVATION FUNCTION
# calc_score_activation = lambda freq : (exp(freq) / (exp(freq) + 1))
calc_score_activation = lambda freq : freq

def score_token_importance(rawSearch, tokenSet, freqDict):
    """
    Attempts to find the importance of a token to a search by leveraging
    ML models, token frequency, and posting list lengths
    """
    # maskedWeights = Counter(get_masked_weights(tokenSet, rawSearch))
    # tokens are ranked with td-idf schema using freqDict: tokenScore = inverseDocumentFreq * termFreq
    tokenScores = {token:(calc_score_activation(1/freqDict[token][0])) for token in tokenSet}
    # numPoints = sum([tokenScores[token] for token in tokenScores])
    # print(numPoints)
    # tokenScores = dict(map(lambda elt : (tokenScores[elt] / numPoints), tokenScores))
    # print(tokenScores)
    return tokenScores