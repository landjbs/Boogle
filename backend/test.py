from models.knowledge.knowledgeBuilder import vector_update_corrDict

vector_update_corrDict('data/inData/wikipedia_utf8_filtered_20pageviews.csv', {'harvard yard':[(0, 'harvard college'),
                                                                                                (0,'james joyce'),
                                                                                                (0, 'montana'),
                                                                                                (0, 'boston')],
                                                                                'harvard college':[],
                                                                                'james joyce':[],
                                                                                'montana':[],
                                                                                'boston':[]})



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
