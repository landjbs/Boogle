import models.knowledge.knowledgeBuilder as knowledgeBuilder
import re

knowledgeSet = knowledgeBuilder.build_knowledgeSet('data/inData/wikiTitles.txt',
                                                    'data/outData/knowledge/knowledgeSet.sav')

knowledgeProcessor = knowledgeBuilder.build_knowledgeProcessor('data/outData/knowledge/knowledgeSet.sav'
                                                                'data/outData/knowledge/knowledgeProcessor.sav')

test = knowledgeBuilder.build_freqDict("data/outData/dmozProcessed/Arts", knowledgeProcessor, 'data/outData/knowledge/freqDict.sav')

print(test['harvard'])
