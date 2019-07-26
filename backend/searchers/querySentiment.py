"""
Scripts to analyze the sentiment of a search query. Methods
include finding the importance of each token as well as removing
stop words, classifying the search desire, and determining
locational/temporal tokens
"""

import numpy as np
from math import exp
from collections import Counter
from keras.models import load_model

from models.binning.docVecs import vectorize_doc

# model to determine whether or not the query is in question form
formatModel = load_model('backend/data/outData/searchAnalysis/questionFormatModel.sav')

# calc_score_activation = lambda freq : exp(freq) / (exp(freq) + 1)
calc_score_activation = lambda freq : freq

def score_token_importance(cleanedSearch, tokenSet, freqDict):
    """
    Attempts to find the importance of a token to a search by leveraging
    ML models, token frequency, and posting list lengths
    """
    tokenScores = {token : calc_score_activation(freqDict[token][0])
                    for token in tokenSet}
    searchVec = vectorize_doc(cleanedSearch)
    # whether the query is in question form (eg. "what is the best search engine?")
    questionFormat = True if (formatModel.predict(np.expand_dims(searchVec, axis=0)[0][0])>0.9) else False
    print(questionFormat)
    return (tokenScores, searchVec)
