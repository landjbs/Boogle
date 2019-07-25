from models.knowledge.knowledgeBuilder import build_corr_dict, build_knowledgeProcessor
from dataStructures.objectSaver import load
freqDict = load('data/outData/knowledge/freqDict.sav')

while True:
    s = input('search: ')
    try:
        print(freqDict[s])
    except Exception as e:
        print(e)
