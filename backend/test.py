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
# import models.binning.docVecs as docVecs

from models.binning.clustering import cluster_given_centroids

freqDict = load('data/outData/knowledge/freqDict.sav')

freqList = [token for i, token in enumerate(freqDict) if not i > 300]

x = cluster_given_centroids(['easter', 'helicopter', 'italy', 'steak'], freqDict, display=True)

while True:
    cluster = input('search: ')
    print(x[cluster][:15])

# while True:
#     new = input("search: ")
#     newVec = docVecs.vectorize_doc(new)
#     scoreLambda = lambda tokenTuple : (euclidean(tokenTuple[0], newVec), tokenTuple[1])
#     scoredDocs = list(map(scoreLambda, vecList))
#     scoredDocs.sort()
#     print('\tRelated Searches:')
#     for tokenTuple in scoredDocs:
#         print(f"\t{tokenTuple[1]}: {tokenTuple[0]}")
