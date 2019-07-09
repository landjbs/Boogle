import re
import os
import numpy as np
import pandas as pd
from termcolor import colored
import matplotlib.pyplot as plt
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import cosine, euclidean
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

from dataStructures.objectSaver import load
from models.knowledge.knowledgeFinder import find_rawTokens
from models.ranking.distributionRanker import rank_distribution
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
import models.binning.docVecs as docVecs

knowledgeProcessor = build_knowledgeProcessor({'harvard'})

# freqDict = load('data/outData/knowledge/freqDict.sav')

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

# while True:
#     new = input("search: ")
#     newVec = docVecs.vectorize_doc(new)
#     scoreLambda = lambda tokenTuple : (euclidean(tokenTuple[0], newVec), tokenTuple[1])
#     scoredDocs = list(map(scoreLambda, vecList))
#     scoredDocs.sort()
#     print('\tRelated Searches:')
#     for tokenTuple in scoredDocs:
#         print(f"\t{tokenTuple[1]}: {tokenTuple[0]}")
