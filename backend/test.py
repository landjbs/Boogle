import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
import crawlers.htmlAnalyzer as ha
import models.processing.cleaner as cleaner

while True:
    url = input("Search: ")
    try:
        print(ha.get_pageText(url))
    except Exception as e:
        print(e)


# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
#
# test = knowledgeBuilder.build_freqDict("data/outData/dmozProcessed/Arts", knowledgeProcessor, 'data/outData/knowledge/freqDict.sav')
#
# print(test['harvard'])
