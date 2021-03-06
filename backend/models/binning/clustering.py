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


class FuzzyVec():
    """ Class to store a single embeded string/vector and pointers to neighbors """
    def __init__(self, name):
        self.name = name
        self.vec = docVecs.vectorize_doc(name)
        self.neighbors = []

    def find_nearest(self, fuzzyVecList, cutoff):
        """
        Finds neighbors in list of FuzzyVec()s within cutoff distance and
        stores in ranked list of (dist, FuzzyVec)
        """
        selfVec = self.vec
        neighbors = []
        for fuzzyObj in fuzzyVecList:
            if not fuzzyObj == self:
                curDist = euclidean(fuzzyObj.vec, selfVec)
                if (curDist < cutoff):
                    neighbors.append((curDist, fuzzyObj))
        neighbors.sort()
        self.neighbors = neighbors



# class FuzzyStore():
#     """ Class to store nearest neighbors of FuzzyVecs """
#     def __init__




class ClusterElement():
    """ Class to define an object in a cluster """
    def __init__(self, name, vector):
        self.name = name
        self.vector = vector

class Cluster():
    """ Class to define a cluster of ClusterElements """
    def __init__(self, name, center):
        self.name = name
        self.center = center
        self.elements = []

    def distance(self, documentVector, distance_function):
        """
        Finds distance between Cluster and
        ClusterElement using distance_function
        """
        return distance_function(self.center, documentVector)

    def add_element(self, element, distance):
        """ Adds element with distance from cluster center to cluster """
        self.elements.append()

def cluster_given_centroids(centroids, data, maxDist=100, distanceMetric='euclidean', displayContents=False, plotRelation=False):
    """
    Args:
        -centroids:         list of strings to act as centroids around which clusters will be computed
        -data:              list of strings to cluster around centroids
        -maxDist:           maximum distance at which a data vector can count for a cluster (defaults to 100)
        -distanceMetric:    distanceMetric to use when calculating distance between data vector and centroid
        -displayContents:   whether to display the cluster contents after clustering
        -plotRelation:      whether to plot force-directed graph of cluster relationships
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

    for i, observation in enumerate(data):
        if not observation=="":
            observationVec = docVecs.vectorize_doc(observation)
            distanceDict = {centroid:(calc_dist(observationVec, centroidScores[centroid]))
                            for centroid in centroids}
            cluster = min(distanceDict, key=(lambda elt : distanceDict[elt]))
            clusters[cluster].append(observation)
        print(f'Clustering: {i}', end='\r')
    print('\n')
    if displayContents:
        for cluster in clusters:
            print(f'Centroid: {cluster}')
            for element in clusters[cluster]:
                print(f'\t-{element}')

    # if plotRelation:


    return clusters
