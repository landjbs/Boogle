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
from scipy.special import softmax
import tensorflow as tf
from models.binning.docVecs import vectorize_doc
from dataStructures.objectSaver import load
from keras.models import load_model

# list of words to remove from queryFormat == question
QUESTION_STOP_WORDS = ['what', 'who', 'why', 'when', 'how', 'in', 'the',
                        'a', 'is', 'was', 'did', 'will']

# model to determine whether or not the query is in question form
formatModel = load_model('backend/data/outData/searchAnalysis/queryFormatModel.h5')
global graph
graph = tf.get_default_graph()

# calc_score_activation = lambda freq : exp(freq) / (exp(freq) + 1)
calc_score_activation = lambda freq : (1/freq)

def score_token_importance(cleanedSearch, tokenSet, freqDict):
    """
    Attempts to find the importance of a token to a search by leveraging
    ML models, token frequency, and posting list lengths
    """
    searchVec = vectorize_doc(cleanedSearch)
    with graph.as_default():
        formatPrediction = formatModel.predict(np.expand_dims(searchVec, axis=0))
    queryFormat = 'question' if (formatPrediction > 0.4) else 'keyword'
    if queryFormat == 'question':
        tokenSet = {token for token in tokenSet
                    if not token in QUESTION_STOP_WORDS}
        print(tokenSet)

    tokenScores = {token : calc_score_activation(freqDict[token][0])
                    for token in tokenSet}

    # normalize token scores
    # tokenScores = softmax(tokenScores.values())
    return (tokenScores, searchVec, queryFormat)
