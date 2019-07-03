"""
Ranks documents on the similarity between their parts. More diverse documents
will have higher scores for the same token frequency than less diverse documents.
"""

from models.binning.docVecs import vectorize_all, vectorize_n_split
from scipy.spatial.distance import euclidean
import numpy as np

def rank_distribution(document, n=5, distanceMetric='dot'):
    """
    Gives document ranking on similarity between n-split document vectors
    """
    baseVec = vectorize_all(document)

    vecMatrix = vectorize_n_split(document, n)

    scores = [np.dot(curVec, baseVec) for curVec in vecMatrix]

    meanScore = np.mean(scores)

    normedScores = [score/meanScore for score in scores]

    uniformity = round(euclidean(normedScores, [0 for _ in range(n)]), 2)

    return uniformity
