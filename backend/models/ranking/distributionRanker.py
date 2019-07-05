"""
Ranks documents on the similarity between their parts. More diverse documents
will have higher scores for the same token frequency than less diverse documents.
"""

from models.binning.docVecs import vectorize_doc, vectorize_n_split
from scipy.spatial.distance import euclidean
import numpy as np

def rank_distribution(document, n=5, distanceMetric='dot'):
    """
    Gives document ranking on similarity between n-split document vectors
    """
    # vectorize entire document
    baseVec = vectorize_all(document)
    # get matrix of document as vectors of n chunks
    vecMatrix = vectorize_n_split(document, n)
    # score dot product between each chunk and base vec
    scores = [np.dot(curVec, baseVec) for curVec in vecMatrix]
    # scores = [np.sum([np.dot(curVec, other) for other in vecMatrix]) for curVec in vecMatrix]
    # normalize scores relative to mean
    meanScore = np.mean(scores)
    # calculate distance between each score and uniform dist around mean
    uniformityScore = round(euclidean(scores, [meanScore for _ in range(n)]), 2)
    return uniformityScore
