from time import time
import numpy as np
import matplotlib.pyplot as plt

from collections import Counter
from dataStructures.objectSaver import load
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeBuilder import (build_token_relationships,
                                                build_corr_dict,
                                                build_knowledgeProcessor,
                                                vector_update_corrDict)
from models.knowledge.knowledgeFinder import score_divDict

# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
freqDict = load('data/outData/knowledge/freqDict.sav')

title = 'harvard university'
all = 'harvard university is a liberal arts university in cambridge massachusets. it has 16000 undergraduates and 20000 associates. famous alumni include boogle founder, landon smith, and facebook founder, mark zuckerberg.'

specialSet = {'harvard university', 'liberal arts', 'liberal arts university',
            'cambridge massachusets', 'mark zuckerberg', 'landon smith'}
for word in (title.split() + all.split()):
    specialSet.add(word)
knowledgeProcessor = build_knowledgeProcessor(specialSet)

while True:
    divDict = {'title':title, 'all':all}
    print(score_divDict(divDict, knowledgeProcessor, freqDict))
    title = input('title: ')
    all = input('all: ')
    words = set(title.split() + all.split())
    # knowledgeProcessor = build_knowledgeProcessor(words)

# establish paths
FREQ_PATH = 'data/outData/knowledge/freqDict.sav'
WIKI_PATH = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'


# # load freqDict and choose some sub selection if desired
# freqDict = load(FREQ_PATH)
# freqKeys = [token for token in freqDict.keys()]
#
# myTokens = ['computer game', 'video game', 'play station', 'gameboy', 'speakers',
#             'television', 'arcade', 'xbox', 'radio', 'music', 'programming',
#             'coding', 'store', 'invention', 'microwave', 'refrigerator',
#             'python', 'java', 'programming language', 'violence', 'concern',
#             'parents', 'children', 'kids', 'developer', 'battle', 'knight',
#             'film', 'movie', 'critic', 'rotten tomatoes', 'pixar', 'film studio',
#             'animated short', 'best', 'favorite', 'top', 'coffee',
#             'starbucks', 'dunkin donuts', 'knight', 'fortress', 'castle',
#             'frappe', 'espresso', 'wood', 'log', 'cabin', 'forest', 'axe',
#             'tree', 'chainsaw', 'forester', 'logging', 'catapult', 'crosbow',
#             'arrow', 'fire', 'forest']
#
# myFreqs = {token : freqDict[token]
#             for token in myTokens if token in freqDict}
#
# corrDict = build_corr_dict(filePath=WIKI_PATH, freqDict=myFreqs,
#                     outPath='data/outData/knowledge/corrDict.sav')
#
# print(corrDict)

# corrDict = load('data/outData/knowledge/corrDict.sav')

while True:
    s = input('S: ')
    if s == '//':
        break
    try:
        print(f'\t{s}')
        for elt in corrDict[s][:5]:
            print(f'\t\t{elt[0]}> {elt[1]}')
    except Exception as e:
        print(f'ERROR: {e}')


vecCorrDict = vector_update_corrDict(WIKI_PATH, corrDict, corrWeight=0.6,
    tokenWeight=0.2, textWeight=0.2,
    outPath='data/outData/knowledge/relationshipDict.sav')

while True:
    s = input('S: ')
    if s == '//':
        break
    try:
        print(f'\t{s}')
        for elt in vecCorrDict[s]:
            print(f'\t\t<{elt[0]}> {elt[1]}')
    except Exception as e:
        print(f'ERROR: {e}')
