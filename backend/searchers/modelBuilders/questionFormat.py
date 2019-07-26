"""
Uses data gathered from the Google Natural Question dataset to build a model
that can differentiate between a keyword query (eg. boogle best) and a
question query (eg. is boogle the best?)
"""

import numpy as np
import pandas as pd

from dataStructures.objectSaver import load, save
from models.binning.docVecs import vectorize_doc

freqDict = load('data/outData/knowledge/freqDict.sav')

def create_fake_queries(queryNum, queryLen=9, outPath=None):
    """
    Build dataframe of freq-weighted random word queries of
    len==(normal around queryLen) and thier vectors
    """

    def unzip_freqDict(d):
        tokens, freqs = [], []
        for key,val in d.items():
            tokens.append(key)
            freqs.append(val[0])
        return tokens, np.array(freqs)

    tokens, freqs = unzip_freqDict(freqDict)
    freqs /= freqs.sum()

    words = np.random.choice(tokens, size=queryNum, replace=True, p=freqs)
    chunks = [max(int(chunk), 1) for chunk in np.random.normal(queryLen, size=queryNum)]
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


fakeQueryDf = scramble_fake_queries(6215)
