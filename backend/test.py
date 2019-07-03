import matplotlib.pyplot as plt
from termcolor import colored
import numpy as np
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from models.knowledge.knowledgeFinder import find_rawTokens
import re
import os
from scipy.spatial.distance import euclidean
from sklearn.metrics.pairwise import cosine_similarity
from crawlers.htmlAnalyzer import get_pageText
import pandas as pd
import models.binning.docVecs as docVecs
from models.ranking.distributionRanker import rank_distribution

print(colored('Imports complete', 'cyan'))



# import appscript
# appscript.app('Terminal').do_script('bert-serving-start -model_dir /Users/landonsmith/Desktop/uncased_L-24_H-1024_A-16 -num_worker=1')

while True:
    # url = input('url: ')
    cleanText = input('test: ')
    print(rank_distribution(cleanText, 5))


def bert_arthimetic(inStr):
    """ inStr must have form 'TERM_1 [+|-] TERM_2 '"""
    splitStrs = inStr.split()
    numTokens = len(splitStrs)

    if (numTokens==1):
        return bc.encode(splitStrs)[0]

    elif (numTokens==3):
        operator = splitStrs[1]
        vecs = bc.encode([splitStrs[0], splitStrs[2]])
        # identify arthimetic method
        if (operator=='+'):
            return np.add(vecs[0], vecs[1])
        elif (operator=='-'):
            return np.subtract(vecs[0], vecs[1])
        else:
            raise ValueError('Invalid operator')



def vectorize_masked_tokens(document, maskToken='', knowledgeProcessor=None, scoringMethod='euclidean', disp=False):
    """
    Iteratively masks all knowledge tokens in document string and determines
    score relative to initial vector. Returns dict of token and score
        -document: string of the document to vectorize
        -maskToken: string to replace each token with
        -knowledgeProcessor: knowledge tokens to locate, will be built from document if not given
        -scoringMethod: use euclidean distance or dot product to determine distance from baseVec
        -disp: whether to display the bar chat of distances
    """
    # assertions and special conditions
    assert isinstance(document, str), "document must have type 'str'"
    assert isinstance(maskToken, str), "maskToken must have type 'str'"
    assert (scoringMethod in ['euclidean', 'dot']), "scoringMethod must be 'euclidean' or 'dot'"

    if not knowledgeProcessor:
        knowledgeProcessor = build_knowledgeProcessor(document.split())

    # define scoring method
    if (scoringMethod=='euclidean'):
        def calc_score(maskedVec, baseVec):
            return euclidean(maskedVec, baseVec)
    elif (scoringMethod=='dot'):
        def calc_score(maskedVec, baseVec):
            return np.sum(maskedVec * baseVec) / np.linalg.norm(baseVec)

    # calculate vector of raw document
    baseVec = bc.encode([document])[0]

    # find tokens in document with both greedy and non-greedy matching
    foundTokens = find_rawTokens(document, knowledgeProcessor)

    scoreDict = {}

    for token in foundTokens:
        print(colored(f'\t{token}', 'red'), end=' | ')
        maskedDoc = re.sub(token, maskToken, document)
        maskedVec = bc.encode([maskedDoc])[0]
        score = calc_score(maskedVec, baseVec)
        print(colored(score, 'green'))
        scoreDict.update({token:score})

    if disp:
        plt.bar(scoreDict.keys(), scoreDict.values())
        plt.ylabel('Euclidean Distance from Base Vector')
        plt.title(f'Tokens Iteratively Replaced With "{maskToken}"')
        plt.show()

    return scoreDict


def word_vs_sentence(document):
    tokens = document.split()

    docVec = bc.encode([document])[0]

    vecList = [bc.encode([token])[0] for token in tokens]

    maxList = []

    for i, vec in enumerate(vecList):
        cumDist = np.sum([euclidean(vec, other) for other in vecList])
        print(tokens[i], cumDist)
        maxList.append((cumDist, tokens[i]))

    print(f"\n{max(maxList)}\n")
