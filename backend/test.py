from models.knowledge.knowledgeBuilder import build_token_relationships, build_corr_dict, build_knowledgeProcessor

freqDict = {'harvard':(0.00001, 1), 'college':(0.00001, 1), 'juice':(0.00001, 1)}
knowledgeProcessor = build_knowledgeProcessor(freqDict.keys())

print(build_corr_dict('data/inData/wikipedia_utf8_filtered_20pageviews.csv', knowledgeProcessor, freqDict))



# from models.knowledge.knowledgeBuilder import build_corr_dict, build_knowledgeProcessor
# from dataStructures.objectSaver import load
#
# freqDict = load('data/outData/knowledge/freqDict.sav')
# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
# # knowledgeProcessor = build_knowledgeProcessor({'harvard', 'college', 'university', 'classes', 'james', 'john', 'door'})
#
# build_corr_dict('data/inData/wikipedia_utf8_filtered_20pageviews.csv',
#                 knowledgeProcessor=knowledgeProcessor,
#                 freqDict=freqDict,
#                 outPath='data/outData/knowledge/corrDict.sav')
#
#
# # for key,val in (load('data/outData/knowledge/corrDict.sav')).items():
# #     print(f'{key}\n\t{val}')
