from dataStructures.objectSaver import load
from models.knowledge.knowledgeBuilder import (build_token_relationships,
                                                build_corr_dict,
                                                build_knowledgeProcessor,
                                                vector_update_corrDict)

FREQ_PATH = 'data/outData/knowledge/freqDict.sav'
WIKI_PATH = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'

freqDict = load(FREQ_PATH)
myTokens = ['coffee', 'starbucks', 'dunkin donuts', 'joe and the juice',
            'wood', 'cabin', 'logs', 'residue', 'espresso']
myFreqs = {token:val for token, val in freqDict.items() if token in myTokens}


corrDict = build_corr_dict(WIKI_PATH, myFreqs)
print(corrDict)

while True:
    s = input('S: ')
    try:
        print(f'\t{s}')
        for elt in d[s]:
            print(f'\t\t{elt[0]}> {elt[1]}')
    except Exception as e:
        print(f'ERROR: {e}')
