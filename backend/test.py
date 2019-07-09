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

print(colored('Imports complete', 'cyan'))

# from models.binning.bertAnalytics import bert_parser

knowledgeProcessor = build_knowledgeProcessor({'harvard'})


# freqDict = load('data/outData/knowledge/freqDict.sav')

freqDict = {'christmas', 'halloween', 'thanksgiving', 'car', 'truck', 'helicopter'}

# tokenList = freqDict.keys()
# vecList = docVecs.score_doc_list(tokenList)

vecList = []
for token in freqDict.keys():
    # tokenVec = docVecs.vectorize_doc(token)
    tokenVec = {'0':0, '1':1}
    vecDict = docVecs.vec_to_dict(tokenVec)
    vecDict.update({'token':token})
    vecList.append(vecList)

print(vecList[:5])



vecDF = pd.DataFrame(vecList)

print(vecDF.head())


# while True:
#     new = input("search: ")
#     newVec = docVecs.vectorize_doc(new)
#     scoreLambda = lambda tokenTuple : (euclidean(tokenTuple[0], newVec), tokenTuple[1])
#     scoredDocs = list(map(scoreLambda, vecList))
#     scoredDocs.sort()
#     print('\tRelated Searches:')
#     for tokenTuple in scoredDocs:
#         print(f"\t{tokenTuple[1]}: {tokenTuple[0]}")
