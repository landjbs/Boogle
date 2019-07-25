from models.knowledge.knowledgeBuilder import build_corr_dict, build_knowledgeProcessor
from dataStructures.objectSaver import load
freqDict = load('data/outData/knowledge/freqDict.sav')
knowledgeProcessor = build_knowledgeProcessor({'the', 'test', 'a'})
build_corr_dict('data/inData/wikipedia_utf8_filtered_20pageviews.csv', knowledgeProcessor, freqDict)
