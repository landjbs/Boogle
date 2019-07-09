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


def cluster_given_centroids(centroids, data, maxDist=100, distanceMetric='euclidean'):
    """
    Args:
        -centroids:         list of strings to act as centroids around which clusters will be computed
        -data:              list of strings to cluster around centroids
        -maxDist:           maximum distance at which a data vector can count for a cluster (defaults to 100)
        -distanceMetric:    distanceMetric to use when calculating distance between data vector and centroid
    """
    assert isinstance(centroids, list), "centroids must have type 'list'."
    assert isinstance(data, list), "data must have type 'list'."
    assert isinstance(maxDist, int), "maxDist must have type 'int'."

    if distanceMetric=='euclidean':
        def calc_dist(vec1, vec2): return euclidean(vec1, vec2)
    elif distanceMetric=='dot':
        def calc_dist(vec1, vec2): return np.dot(vec1, vec2)
    elif distanceMetric=='cos':
        def calc_dist(vec1, vec2): return cosine(vec1, vec2)
    else:
        raise ValueError(f"Invalid distance metric '{distanceMetric}'.")




freqDict = {'christmas', 'halloween', 'thanksgiving', 'automobile', 'car', 'truck', 'helicopter', 'pie', 'jelly', 'bacon', 'usa', 'canada', 'iran'}

centroids = ['easter', 'airplane', 'sausage', 'syria']
centroidDict = {token:(docVecs.vectorize_doc(token)) for token in centroids}
clusters = {centroid:[] for centroid in centroids}

for token in freqDict:
    tokenVec = docVecs.vectorize_doc(token)
    distDict = {centroid:(euclidean(tokenVec, centroidDict[centroid])) for centroid in centroidDict}
    cluster = min(distDict, key=(lambda elt:distDict[elt]))
    print(f'{token}: {cluster}')
    clusters[cluster].append(token)

for cluster in clusters:
    print(f'{cluster}')
    for elt in clusters[cluster]:
        print(f'\t-{elt}')
