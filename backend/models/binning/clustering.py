"""
Implementation of clustering algorithms to find groupings in a list of
document vectors generated with the BERT model in models/binning/docVecs.py.
These clusters are used to define bins within the value portion of the
topDict key-val store implemented in dataStructures/thicctable.py.
By creating a second key-val mapping within the keyword-oriented topDict,
I hope to allow a smaller database to provide more comprehensive search
results than simple keyword lookup-tables.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine, euclidean
from sklearn.metrics.pairwise import cosine_similarity

import models.binning.docVecs as docVecs


def cluster_given_centroids(centroids, data, maxDist=100, distanceMetric='euclidean', display=False):
    """
    Args:
        -centroids:         list of strings to act as centroids around which clusters will be computed
        -data:              list of strings to cluster around centroids
        -maxDist:           maximum distance at which a data vector can count for a cluster (defaults to 100)
        -distanceMetric:    distanceMetric to use when calculating distance between data vector and centroid
        -display:           whether to display the clusters after clustering
    """
    # assert arg structure
    assert (len(centroids)>0), "centroids must be iterable of length > 0."
    assert (len(data)>0), "data must be iterable of length > 0."
    assert isinstance(maxDist, int), "maxDist must have type 'int'."
    # determine distance function from arg distanceMetric
    if distanceMetric=='euclidean':
        def calc_dist(vec1, vec2): return euclidean(vec1, vec2)
    elif distanceMetric=='dot':
        def calc_dist(vec1, vec2): return np.dot(vec1, vec2)
    elif distanceMetric=='cos':
        def calc_dist(vec1, vec2): return cosine(vec1, vec2)
    else:
        raise ValueError(f"Invalid distance metric '{distanceMetric}'.")
    # build dict of
    centroidScores = {centroid:(docVecs.vectorize_doc(centroid))
                        for centroid in centroids}
    clusters = {centroid:[] for centroid in centroids}

    for observation in data:
        if not observation=="":
            observationVec = docVecs.vectorize_doc(observation)
            distanceDict = {centroid:(calc_dist(observationVec, centroidScores[centroid]))
                            for centroid in centroids}
            cluster = min(distanceDict, key=(lambda elt : distanceDict[elt]))
            clusters[cluster].append(observation)

    if display:
        for cluster in clusters:
            print(cluster)
            for element in clusters[cluster]:
                print(f'\t-{element}')

    return clusters
