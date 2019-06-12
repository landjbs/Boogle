import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load

# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')

# test = knowledgeBuilder.build_freqDict("data/outData/dmozProcessed/Arts", knowledgeProcessor, 'data/outData/knowledge/freqDict.sav')

test = load('data/outData/knowledge/freqDict.sav')

scores = []
for item in test:
    scores.append(test[item])

for item in test:
    if test[item] == max(scores):
        print(item)
