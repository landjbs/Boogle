"""
Ranks documents on the similarity between their parts. More diverse documents
will have higher scores for the same token frequency than less diverse documents.
"""

from models.binning.docVecs import vectorize_doc, vectorize_n_split
from scipy.spatial.distance import cosine, euclidean
from numpy import mean

def rank_distribution(document, n=5, distanceMetric='dot'):
    """
    Gives document ranking on similarity between n-split document vectors
    """
    # vectorize entire document
    baseVec = vectorize_all(document)
    # get matrix of document as vectors of n chunks
    vecMatrix = vectorize_n_split(document, n)
    # score dot product between each chunk and base vec
    scores = [cosine(curVec, baseVec) for curVec in vecMatrix]
    meanScore = np.mean(scores)
    # calculate distance between score distribution and uniform distribution around mean
    uniformityScore = round(euclidean(scores, [meanScore for _ in range(n)]), 2)
    return uniformityScore
