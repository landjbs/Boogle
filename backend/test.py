from os import listdir
from numpy import dot
from tqdm import tqdm
import matplotlib.pyplot as plt

from dataStructures.objectSaver import load
from models.knowledge.knowledgeNetwork import build_corr_dict
from models.knowledge.knowledgeBuilder import vector_update_corrDict
from models.knowledge.shadowTokenization import add_shadow_tokens

filePath = 'data/thicctable/wikiCrawl_SHADOW_NOVECS'

corrDict = load('data/outData/knowledge/corrDict_SINGLE_WORD.sav')

for i, file in enumerate((listdir(filePath))):
    try:
        pageList = load(f'{filePath}/{file}')
        for pageDict in pageList:
            print(pageDict['title'])
            knowledgeTokens = pageDict['knowledgeTokens']
            shadowTokens = add_shadow_tokens(knowledgeTokens.copy(), corrDict, cutoff=0.1)
            for token, score in shadowTokens.items():
                if not token in knowledgeTokens:
                    print(f'\t<{score}> {token}')
                else:
                    print(f'IS: {token}')
            # plt.bar(tokens.keys(), tokens.values())
            # plt.title(pageDict['title'])
            # plt.show()
    except Exception as e:
        print(f'{e} at "{file}".')

# relationshipDict = vector_update_corrDict('wikipedia_utf8_filtered_20pageviews.csv',
#     corrDict, outPath='data/outData/knowledge/relationshipDict.sav')
#
# print(relationshipDict.keys())
#
# while True:
#     s = input('search: ')
#     try:
#         for elt in relationshipDict[s]:
#             print(f'\t<{elt[0]}> {elt[1]}')
#     except KeyError:
#         print('\tToken not found.')


# freqDict = load('data/outData/knowledge/freqDict.sav')
#
# corrDict = (build_corr_dict('data/thicctable/wikiCrawl_SHADOW_NOVECS',
#                 freqDict=freqDict,
#                 outPath='data/outData/knowledge/corrDict_SINGLE_WORD.sav'))
