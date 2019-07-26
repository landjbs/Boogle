import numpy as np
import pandas as pd

from dataStructures.objectSaver import load, save
from models.binning.docVecs import vectorize_doc

freqDict = load('data/outData/knowledge/freqDict.sav')

def unzip(d):
    tokens, freqs = [], []
    for key,val in d.items():
        tokens.append(key)
        freqs.append(val[0])
    return tokens, np.array(freqs)


def scramble_fake_queries(queryNum, queryLen=9, outPath=None):
    """
    Scramble up knowlege tokens for random sents
    """
    tokens, freqs = unzip(freqDict)
    freqs /= freqs.sum()

    words = np.random.choice(tokens, size=queryNum, replace=True, p=freqs)
    chunks = [max(int(chunk), 1) for chunk in np.random.normal(4, size=queryNum)]
    print(len(words), len(chunks))

    queryList = []

    for i in range(len(words)):
        print(f'Building: {i}', end='\r')
        chunkSteps = chunks[i]
        if ((queryNum - i) > chunkSteps):
            sent = " ".join(words[i : (i + chunkSteps)])
        else:
            sent = " ".join(words[i : (i + (queryNum - i))])
        vec = vectorize_doc(sent)
        queryList.append({'query':sent, 'vec':vec})


    queryDf = pd.DataFrame(queryList)

    if outPath:
        queryDf.to_pickle(outPath)

    return queryDf


print(scramble_fake_queries(6215, "fakeQueryDf.sav"))
