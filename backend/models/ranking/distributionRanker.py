"""
Ranks documents on the similarity between their parts. More diverse documents
will have higher scores for the same token frequency than less diverse documents.
"""

from models.binning.docVecs import vectorize_doc, vectorize_n_split
from scipy.spatial.distance import cosine, euclidean
from numpy import mean

def rank_distribution(document, n=5):
    """
    Gives document ranking on similarity between n-split document vectors.
    High diversityScore means that the page has more diversity between its
    compontents
    """
    # vectorize entire document
    baseVec = vectorize_doc(document)
    # get matrix of document as vectors of n chunks
    vecMatrix = vectorize_n_split(document, n)
    # score cosine similarity between each chunk and base vec
    scores = [cosine(curVec, baseVec) for curVec in vecMatrix]
    print(scores)
    meanScore = mean(scores)
    print(meanScore)
    # calculate distance between score distribution and uniform distribution around mean
    diversityScore = round(euclidean(scores, [meanScore for _ in range(n)]), 2)
    return diversityScore
