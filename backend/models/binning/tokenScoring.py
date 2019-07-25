import re
from numpy import sum
from scipy.spatial.distance import euclidean

import models.binning.docVecs as docVecs

MASK_TOKEN = ""


def score_single_token(token, document, baseVec):
     maskedDoc = re.sub(token, MASK_TOKEN, document)
     maskedVec = docVecs.vectorize_doc(maskedDoc)
     return euclidean(maskedVec, baseVec)


def get_masked_weights(tokenSet, document):
    """
    Iteratively masks all knowledge tokens in document string and determines
    score relative to initial vector. Returns dict of token and score
    """
    # calculate vector of raw document
    baseVec = docVecs.vectorize_doc(document)
    # calculate the raw score of each token
    scoreDict = {token:(score_single_token(token, document, baseVec))
                for token in tokenSet}
    # normalize score dict by the aggregate of all points
    pointsNum = sum([scoreDict[token] for token in scoreDict])
    print(pointsNum)
    return {token:(score/pointsNum) for token, score in scoreDict.items()}
