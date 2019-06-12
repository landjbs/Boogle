import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load

knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')

test = knowledgeBuilder.build_freqDict("data/outData/dmozProcessed/Arts", knowledgeProcessor, 'data/outData/knowledge/freqDict.sav')

print(test['harvard'])
