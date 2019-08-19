from os import listdir
from numpy import dot
from tqdm import tqdm

from dataStructures.objectSaver import load
from models.knowledge.knowledgeNetwork import build_corr_dict
from models.knowledge.knowledgeBuilder import vector_update_corrDict

wikiPath = 'data/thicctable/wikiCrawl_SHADOW_NOVECS'

freqDict = load('data/outData/knowledge/freqDict.sav')

with open('data/inData/commonWords.txt', 'r') as wordsFile:
    tokenFreqs = {line.strip():(freqDict[line.strip()]) for line in tqdm(wordsFile)
                    if line.strip() in freqDict}
print(len(tokenFreqs))

corrDict = (build_corr_dict('data/thicctable/wikiCrawl_SHADOW_NOVECS',
                freqDict=tokenFreqs,
                outPath='data/outData/knowledge/corrDict_NEW.sav'))
