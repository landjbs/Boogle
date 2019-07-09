import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from models.knowledge.knowledgeFinder import find_rawTokens
import re
import os
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity
from crawlers.htmlAnalyzer import get_pageText
import pandas as pd
from models.ranking.distributionRanker import rank_distribution
from dataStructures.objectSaver import load
from scipy.spatial.distance import cosine, euclidean

import models.binning.docVecs as docVecs

print(colored('Imports complete', 'cyan'))

# from models.binning.bertAnalytics import bert_parser

knowledgeProcessor = build_knowledgeProcessor({'harvard'})

import matplotlib.pyplot as plt

while True:
    doc = input('doc: ')
    vec = docVecs.vectorize_doc(doc)
    plt.plot(vec)
    plt.show()

# freqDict = load('data/outData/knowledge/freqDict.sav')

# tokenList = [token for token in freqDict]

# print(tokenList[:4])

# vecList = docVecs.score_doc_list(tokenList)

# print(vecList)

# while True:
#     new = input("search: ")
#     newVec = docVecs.vectorize_doc(new)
#     scoreLambda = lambda tokenTuple : (euclidean(tokenTuple[0], newVec), tokenTuple[1])
#     scoredDocs = list(map(scoreLambda, vecList))
#     scoredDocs.sort()
#     print('\tRelated Searches:')
#     for tokenTuple in scoredDocs:
#         print(f"\t{tokenTuple[1]}: {tokenTuple[0]}")
