import os
import re
from numpy import log, dot, sum
from tqdm import tqdm
from collections import Counter
from flashtext import KeywordProcessor
from scipy.spatial.distance import cosine

from models.processing.cleaner import clean_text, clean_wiki
import models.knowledge.knowledgeFinder as knowledgeFinder
from dataStructures.objectSaver import (save,
                                        load,
                                        safe_make_folder,
                                        delete_folder)


def build_corr_dict(pageFolderPath, freqDict=None, freqCutoff=0.0007,
                    bufferSize=10000, corrNum=20, outPath=None):
    """
    Builds dict mapping tokens to the ranked list of corrNum tokens with the
    highest normalized co-occurence in previously gathered knowledgeTokens
    from pageFolderPath.
    Args:
        -pageFolderPath:        Path to the folder in which pages are stored
                                    as pickeled lists of pageDicts
        -freqDict:              Dictionary of freq tuples for observed tokens
                                    If no argument is passed, freqDict will be
                                    loaded from default path.
        -freqCutoff:            Upper frequency that a token can have and
                                    still be analyzed.
        -bufferSize:            Number of files to analyze in RAM at one time.
                                    At bufferSize, the current tokenDict is
                                    saved under TEMP_FOLDER_PATH and
                                    deleted from RAM. Since each file is a
                                    pickled list of len n, the number of pages
                                    analyzed before saving a tablet
                                    is (n * bufferSize).
        -corrNum:               Max number of tokens to include in the ranked
                                    corrList of each token.
    Returns:
        Dictionary mapping each qualifying token to a scored and ranked list of
        corrNum relatedTokens with scores as floats in range (0, 1].
    """

    # number of iterations during which to filter out low tokens during fold
    FILTER_BUFFER = 1
    # default freqDict path
    FREQ_PATH = 'data/outData/knowledge/freqDict.sav'
    # set of words to exclude from corrableTokens, no matter what
    STOP_WORDS = {'wiki', 'wikipedia', 'en', 'https', 'http', 'org'}
    # build temporary folder to hold tablets of corrDict for RAM safety
    TEMP_FOLDER_PATH = 'corrDictTablets_NEW'

    if not freqDict:
        freqDict = load(FREQ_PATH)

    # common names are uesd as stop words as well
    with open('data/inData/commonNames.txt', 'r') as nameFile:
        STOP_WORDS.update([line.strip().lower() for line in nameFile])

    # iterate over freqDict, building set of tokens qualifing for correlations
    def corrable(token, freqTuple):
        """ Helper determines if token corr should be taken """
        return  False if ((freqTuple[0]>freqCutoff)
                        or (token.isdigit())
                        or (token in STOP_WORDS)
                        or (len(token) <= 2)
                        or len(token.split()) > 1) else True

    corrableTokens = {token for token, freqTuple in freqDict.items()
                        if corrable(token, freqTuple)}

    # print(corrableTokens)

    safe_make_folder(TEMP_FOLDER_PATH)

    # initialize first empty corrDict
    curCorrTablet = {}
    for i, file in enumerate(tqdm(os.listdir(pageFolderPath))):
        try:
            pageList = load(f'{pageFolderPath}/{file}')
            for pageDict in pageList:
                # pull counter of knowledgeTokens from pageDict
                pageTokens = pageDict['knowledgeTokens']
                # title tokens of a page will be dampened to avoid distortion
                pageTitle = pageDict['title'].lower().strip()
                corrablePageTokens = {token : score
                                        for token, score in pageTokens.items()
                                        if (token in corrableTokens
                                        and token not in pageTitle)}
                for curToken, curFreq in corrablePageTokens.items():
                    curCounter = Counter({otherToken : (otherFreq * curFreq)
                                            for otherToken, otherFreq
                                            in corrablePageTokens.items()
                                            if (otherToken != curToken)})
                    if curToken in curCorrTablet:
                        curCorrTablet[curToken].update(curCounter)
                    else:
                        curCorrTablet.update({curToken : curCounter})
        except Exception as e:
            print(f'ERROR: {e}')
        finally:
            if (i % bufferSize == 0) and (i > 0):
                save(curCorrTablet, f'{TEMP_FOLDER_PATH}/corrTablet{i}.sav')
                curCorrTablet = {}

    # folder saved corrTablets onto most recent corrTablet
    print('Folding tokenDict')
    for i, file in enumerate(tqdm(os.listdir(TEMP_FOLDER_PATH))):
        try:
            loadedCorrTablet = load(f'{TEMP_FOLDER_PATH}/{file}')
            for token, tokenCounter in loadedCorrTablet.items():
                if token in curCorrTablet:
                    curCorrTablet[token].update(tokenCounter)
                else:
                    curCorrTablet.update({token : tokenCounter})
            del loadedCorrTablet
        except Exception as e:
            print(f'ERROR: {e}')
        finally:
            if ((i % FILTER_BUFFER) == 0):
                print(f'Cleaning corrTablet at {i}:', end='\r')
                for token, tokenCounter in tqdm(curCorrTablet.items(), leave=False):
                    counterValues = tokenCounter.values()
                    # if a token has more than corrNum related tokens, filter
                    # the counter down to corrNum and relace larger counter in
                    # curCorrTablet
                    if len(counterValues) > corrNum:
                        sortedValues = [scalar for scalar in counterValues]
                        sortedValues.sort(reverse=True)
                        minScore = sortedValues[corrNum-1]
                        filteredCounter = Counter({relToken : relVal
                                                    for relToken, relVal
                                                    in tokenCounter.items()
                                                    if relVal >= minScore})
                        # print(f'\t{tokenCounter}\n\t{filteredCounter}')
                        curCorrTablet.update({token : filteredCounter})


    def score_to_fraction(tokenTuple, scoreSum):
        """
        Helper converts tokenTuples with rawScores to tokenTuples with
        scores as fractions of topTokens
        """
        return (round((tokenTuple[0] / scoreSum), ndigits=3), tokenTuple[1])


    # build corrDict of top corrNum tokens for each token in tokenDict
    print('Building topTokens')
    corrDict = {}
    for token, counter in tqdm(curCorrTablet.items()):
        corrList = [(score, otherToken)
                    for otherToken, score in counter.items()]
        if corrList != []:
            corrList.sort(reverse=True)

            topTokens = corrList[:corrNum]
            # take sum of scores across top 50 tokens to normalize top scores
            scoreSum = sum([tokenTuple[0] for tokenTuple in corrList[:50]])

            fraction_lambda = lambda tokenTuple : score_to_fraction(tokenTuple,
                                                                    scoreSum)

            topTokens = list(map(fraction_lambda, topTokens))
            corrDict.update({token : topTokens})

    # delete the temporary folder and emptyTokenDict
    delete_folder(TEMP_FOLDER_PATH)

    # save corrDict if prompted
    if outPath:
        save(corrDict, outPath)

    return corrDict
