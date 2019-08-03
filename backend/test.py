from models.knowledge.knowledgeBuilder import build_corr_dict
from dataStructures.objectSaver import load

freqDict = load('data/outData/knowledge/freqDict.sav')
knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
# knowledgeProcessor = build_knowledgeProcessor({'harvard', 'college', 'university', 'classes', 'james', 'john', 'door'})
#
build_corr_dict('data/inData/wikipedia_utf8_filtered_20pageviews.csv',
                knowledgeProcessor=knowledgeProcessor,
                freqDict=freqDict,
                outPath='data/outData/knowledge/corrDict.sav')


# for key,val in (load('data/outData/knowledge/corrDict.sav')).items():
#     if len(val)!=0:
#         print(f'{key}\n\t{val}')
