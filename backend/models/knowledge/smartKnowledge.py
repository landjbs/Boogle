import pandas as pd
from collections import Counter
from keras.models import Sequential
from keras.layers import Dense, Activation

from dataStructures.objectSaver import load
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor


freqCutoff = 0.0007
WIKI_PATH = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'
freqDict = load('data/outData/knowledge/freqDict.sav')

def corrable(token, freqTuple):
    """ Helper determines if token corr should be taken """
    return False if (freqTuple[0]>freqCutoff) or (token.isdigit()) else True

# dict mapping tokens with frequency below freqCutoff to empty counters
corrableTokens = [token for token, freqTuple in freqDict.items()
                    if corrable(token, freqTuple)]

knowledgeProcessor = build_knowledgeProcessor(corrableTokens)


with open(WIKI_PATH, 'r') as wikiFile:
    for line in wikiFile:
        fileTokens = knowledgeProcessor.extract_keywords(line)
        tokenVec = [1 if token in fileTokens else 0 for token in
                    corrableTokens]
        print(tokenVec)
