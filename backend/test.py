import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load

knowledgeSet = load('data/outData/knowledge/knowledgeSet.sav')

print("Loaded!")

knowledgeProcessor = knowledgeBuilder.build_knowledgeProcessor(knowledgeSet, 'data/outData/knowledge/knowledgeProcessor.sav')

test = knowledgeBuilder.build_freqDict("data/outData/dmozProcessed/Arts", knowledgeProcessor, 'data/outData/knowledge/freqDict.sav')

print(test['harvard'])
