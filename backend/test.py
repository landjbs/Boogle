from os import listdir
from numpy import dot
from tqdm import tqdm

from dataStructures.objectSaver import load
from models.knowledge.knowledgeNetwork import build_corr_dict
from models.knowledge.knowledgeBuilder import vector_update_corrDict

corrDict = load('data/outData/knowledge/corrDict_NEW.sav')
print(corrDict.keys())

while True:
    s = input('search: ')
    try:
        for elt in corrDict[s]:
            print(f'\t<{elt[0]}> {elt[1]}')
    except KeyError:
        print('\tToken not found.')


# wikiPath = 'data/thicctable/wikiCrawl_SHADOW_NOVECS'
#
# freqDict = load('data/outData/knowledge/freqDict.sav')
#
# with open('data/inData/commonWords.txt', 'r') as wordsFile:
#     tokenFreqs = {line.strip():(freqDict[line.strip()]) for line in tqdm(wordsFile)
#                     if line.strip() in freqDict}
# print(len(tokenFreqs))
#
# corrDict = (build_corr_dict('data/thicctable/wikiCrawl_SHADOW_NOVECS',
#                 freqDict=tokenFreqs,
#                 outPath='data/outData/knowledge/corrDict_NEW.sav'))
