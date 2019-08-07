import numpy as np
from dataStructures.objectSaver import load
from models.knowledge.knowledgeBuilder import (build_token_relationships,
                                                build_corr_dict,
                                                build_knowledgeProcessor,
                                                vector_update_corrDict)

print(load('data/outData/knowledge/corrDict.sav'))

# establish paths
FREQ_PATH = 'data/outData/knowledge/freqDict.sav'
WIKI_PATH = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'

# load freqDict and choose some sub selection if desired
freqDict = load(FREQ_PATH)

freqKeys = [token for token in freqDict.keys()]

myTokens = ['castle', 'henry viii', 'horse', 'catapult', 'knight',
            'car', 'chess', 'fortress', 'king', 'bus']

myFreqs = {token : freqDict[token]
            for token in myTokens}

corrDict = build_corr_dict(WIKI_PATH, myFreqs)

import matplotlib.pyplot as plt

# corrDict ={'coffee': [(471369940.24214125, 'espresso'), (238482974.2349554, 'dunkin donuts'), (136305343.318782, 'starbucks'), (1030891.7330982436, 'residue'), (697518.602966686, 'wood'), (378287.75076798926, 'cabin'), (178624.0879016093, 'logs')], 'residue': [(2924918.270165199, 'wood'), (2323922.4675443554, 'espresso'), (1030891.7330982436, 'coffee'), (509154.1399538477, 'logs'), (148079.61646287164, 'cabin'), (6719.840195308946, 'starbucks')], 'wood': [(10545018.46488576, 'logs'), (2924918.270165199, 'residue'), (966576.846654676, 'cabin'), (697518.602966686, 'coffee'), (300048.34970461705, 'starbucks'), (229798.86926247875, 'espresso'), (114394.80896480675, 'dunkin donuts')], 'logs': [(15274336.302278876, 'cabin'), (10545018.46488576, 'wood'), (509154.1399538477, 'residue'), (178624.0879016093, 'coffee'), (151672.60268078465, 'starbucks'), (29784.687969318722, 'espresso')], 'cabin': [(15274336.302278876, 'logs'), (966576.846654676, 'wood'), (378287.75076798926, 'coffee'), (262194.87612188945, 'starbucks'), (148079.61646287164, 'residue'), (91408.92232100834, 'espresso')], 'starbucks': [(244032123.67514265, 'espresso'), (136305343.318782, 'coffee'), (42907255.156458475, 'dunkin donuts'), (300048.34970461705, 'wood'), (262194.87612188945, 'cabin'), (151672.60268078465, 'logs'), (6719.840195308946, 'residue')], 'espresso': [(471369940.24214125, 'coffee'), (244032123.67514265, 'starbucks'), (10703821.033933356, 'dunkin donuts'), (2323922.4675443554, 'residue'), (229798.86926247875, 'wood'), (91408.92232100834, 'cabin'), (29784.687969318722, 'logs')], 'dunkin donuts': [(238482974.2349554, 'coffee'), (42907255.156458475, 'starbucks'), (10703821.033933356, 'espresso'), (114394.80896480675, 'wood')]}


while True:
    s = input('S: ')
    try:
        print(f'\t{s}')
        scores = []
        for elt in corrDict[s]:
            print(f'\t\t{elt[0]}> {elt[1]}')
            scores.append(elt[0])
        plt.plot(scores)
        plt.show()
    except Exception as e:
        print(f'ERROR: {e}')
