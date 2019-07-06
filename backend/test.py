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
# import models.binning.docVecs as docVecs
# from models.ranking.distributionRanker import rank_distribution
from dataStructures.objectSaver import load
from scipy.spatial.distance import cosine

print(colored('Imports complete', 'cyan'))

from crawlers.htmlAnalyzer import scrape_url

knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
freqDict = load('data/outData/knowledge/freqDict.sav')

while True:
    url = input('text: ')
    pList = (scrape_url(url, knowledgeProcessor, freqDict))
    print(pList[2])


# import appscript
# appscript.app('Terminal').do_script('bert-serving-start -model_dir /Users/landonsmith/Desktop/uncased_L-24_H-1024_A-16 -num_worker=1')
