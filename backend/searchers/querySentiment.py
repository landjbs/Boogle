"""
Scripts to analyze the sentiment of a search query. Methods
include finding the importance of each token as well as removing
stop words, classifying the search desire, and determining
locational/temporal tokens
"""

import numpy as np
from math import exp
import tensorflow as tf
from scipy.special import softmax
from collections import Counter
from keras.models import load_model

from dataStructures.objectSaver import load
from models.binning.docVecs import vectorize_doc


# list of words to remove from question queryFormat
QUESTION_STOP_WORDS = ['what', 'who', 'why', 'when', 'how', 'in', 'the',
                        'a', 'is', 'was', 'did', 'will']


# model to determine whether or not the query is in question form
formatModel = load_model('backend/data/outData/searchAnalysis/queryFormatModel.h5')
global graph
graph = tf.get_default_graph()

calc_token_importance = lambda freq : (1 / freq)


def score_token_importance(cleanedSearch, tokenSet, database, freqDict):
    """
    Attempts to find the importance of a token to a search by leveraging
    ML models, token frequency, and posting list lengths
    """
    # vectorize the query
    searchVec = vectorize_doc(cleanedSearch)
    # use ML model to predict type of query
    with graph.as_default():
        formatPrediction = formatModel.predict(np.expand_dims(searchVec, axis=0))
    queryFormat = 'question' if (formatPrediction > 0.4) else 'keyword'
    if queryFormat == 'question':
        # remove common question stopwords for question types
        tokenSet = {token for token in tokenSet
                    if not token in QUESTION_STOP_WORDS}

    tokenScores = {token : calc_token_importance(freqDict[token][0])
                    for token in tokenSet}
    print(tokenScores)
    tokenSum = np.sum([score for score in tokenScores.values()])
    normedScores = {token : (rawScore / tokenSum)
                    for token, rawScore in tokenScores.items()}

    # normalize token scores
    return (normedScores, searchVec, queryFormat)
