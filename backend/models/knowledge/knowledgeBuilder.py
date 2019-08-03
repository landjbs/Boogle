"""
Generates set of knowledge tokens, which comprize the keys in the topDict of
the key-val store described in dataStructures.thicctable. These tokens
represent the extent of top-level lookup buckets avaiable to users and, as
such, follow the philosophy of comprehensive concision. There should be enough
knowledge tokens that any reasonable search can be answered by the contents of
a lookup bucket, but not so many as to take up redundant space.
Knowledge tokens are only permitted to be words and phrases; tokens comprised
soley of non-alpha chars will be mapped to the English representation of the
token (eg. & -> ampersand).
These tokens are then converted into a flashtext matcher for ~constant time,
greedy lookup of phrases and words. Flashtext is a great module based on this
paper: https://arxiv.org/pdf/1711.00046.pdf. The matcher is applied in
knowledgeFinder.
"""

import os
import re
from numpy import log
from tqdm import tqdm
from collections import Counter
from flashtext import KeywordProcessor

from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text, clean_wiki
import models.knowledge.knowledgeFinder as knowledgeFinder

## Functions ##
def build_knowledgeSet(knowledgeFile, additionalTokens=None, numberRange=None, outPath=""):
    """
    Args: \n delimited knowledgeFile of phrases to treat as knowledge tokens
    (tokens for strict word search), additionalTokens set of tokens not in
    knowledgeFile, numberRange tuple of range of integer tokens to add, and
    outPath to which to save set
    Returns: set (for fast lookup) of cleaned tokens stripped from knowledgeData
    """
    # open base knowledgeFile
    with open(knowledgeFile) as knowledgeData:
        # build set of cleaned lines in knowledgeData
        knowledgeSet = {clean_wiki(token) for token in knowledgeData}

    # add tokens from additionalTokens set
    if additionalTokens:
        for token in additionalTokens:
            knowledgeSet.add(clean_wiki(token))

    # add integers between first and last elt of numberRange tuple
    if numberRange:
        assert isinstance(numberRange, tuple), "numberRange must be a tuple of integers"
        for num in range(numberRange[0], numberRange[1]):
            knowledgeSet.add(str(num))

    # remove empty token from knowledgeSet (only one because set)
    knowledgeSet.remove("")

    # save knowledge to outPath if specified
    if not (outPath==""):
        save(knowledgeSet, outPath)
    return knowledgeSet


def build_knowledgeProcessor(knowledgeSet, outPath=""):
    """ Builds flashtext matcher for words in knowledgeSet iterable """
    # initialize flashtext KeywordProcessor
    knowledgeProcessor = KeywordProcessor(case_sensitive=False)
    # add all items from knowledge set cast as list
    for i, keyword in enumerate(knowledgeSet):
        print(f"\tBuilding knowledgeProcessor: {i}", end="\r")
        knowledgeProcessor.add_keyword(keyword)
    print("\nknowledgeProcessor Built")
    # save knowledgeProcess to outPath if given
    if not (outPath==""):
        save(knowledgeProcessor, outPath)
    return knowledgeProcessor


def fredDict_from_wikiFile(filePath, knowledgeProcessor, outPath=""):
    """
    Args: filePath to wikiFile containing lines of articles from which to read,
    knowledgeProcessor for token extraction.
    Returns: dict mapping knowledge tokens to tuple of (termFreq, docFreq)
    observed in documents.
        termFreq = (number of times a token is used) / (number of words used)
        docFreq = log ((number of documents) / (number of documents in which a token appears))
    """
    # initialize counter to map knowledge tokens to raw number of occurences
    tokenCounts = Counter()
    # initialize counter to map knowledge tokens to number of docs they appear in
    tokenAppearances = Counter()
    # initialize variable to keep track of total number of words used
    totalLength = 0

    with open(filePath, 'r') as wikiFile:
        for i, line in enumerate(wikiFile):
            # get everything after the first comma
            commaLoc = line.find(',')
            rawText = line[(commaLoc+2):]
            # find the tokens
            tokensFound = knowledgeFinder.find_weighted_tokenCounts(rawText, knowledgeProcessor)
            tokenCounts.update(tokensFound)
            tokenAppearances.update(set(tokensFound))
            totalLength += len(rawText.split())
            print(f"\tBuilding freqDict: {i}", end='\r')

    # lambdas for calculating termFreq and docFreq
    calc_termFreq = lambda tokenCount : tokenCount / totalLength
    calc_docFreq = lambda tokenAppearance : log(float(i) / tokenAppearance)

    # use total num to normalize tokenCounts and find frequency for each token
    freqDict = {token: (calc_termFreq(tokenCounts[token]),
                        calc_docFreq(tokenAppearances[token]))
                for token in tokenCounts}

    if (outPath != ""):
        save(freqDict, outPath)

    return freqDict


def fredDict_from_folderPath(folderPath, knowledgeProcessor, outPath=""):
    """
    Args: folderPath to folder containing files from which to read,
    knowledgeProcessor for token extraction.
    Returns: dict mapping knowledge tokens to tuple of (termFreq, docFreq)
    observed in documents.
        termFreq = (number of times a token is used) / (number of words used)
        docFreq = log ((number of documents) / (number of documents in which a token appears))
    """
    # initialize counter to map knowledge tokens to raw number of occurences
    tokenCounts = Counter()
    # initialize counter to map knowledge tokens to number of docs they appear in
    tokenAppearances = Counter()
    # initialize variable to keep track of total number of words used
    totalLength = 0

    # find and iterate over list of files within folderPath
    for i, file in enumerate(os.listdir(folderPath)):
        print(f"\tBuilding freqDict: {i}", end='\r')
        with open(f"{folderPath}/{file}") as FileObj:
            # read in the current file
            text = FileObj.read()
            # find both greedy and subtokens in text
            tokensFound = list(knowledgeFinder.find_rawTokens(text, knowledgeProcessor))
            # add tokens counts to tokenCounts counter
            tokenCounts.update(tokensFound)
            # add single appearance for each token found
            tokenAppearances.update(set(tokensFound))
            # find number of words in the current file
            textLen = len(text.split())
            # add number of words in current file to totalLength
            totalLength += textLen

    # lambdas for calculating termFreq and docFreq
    calc_termFreq = lambda tokenCount : tokenCount / totalLength
    calc_docFreq = lambda tokenAppearance : log(float(i) / tokenAppearance)

    # use total num to normalize tokenCounts and find frequency for each token
    freqDict = {token: (calc_termFreq(tokenCounts[token]),
                        calc_docFreq(tokenAppearances[token]))
                for token in tokenCounts}

    if (outPath != ""):
        save(freqDict, outPath)

    return freqDict


def build_corr_dict(filePath, knowledgeProcessor, freqDict, freqCutoff=0.0007,
                    bufferSize=4000, corrNum=5, outPath=None):
    """
    Builds dict mapping tokens to the ranked list of corrNum tokens with the
    highest normalized co-occurence in filePath.
    Args:
        -filePath:              Path to the csv file in which the wikipdia
                                    articles are stored
        -knowledgeProcessor:    Flashtext processor for knowledge tokens
        -freqDict:              Dictionary of frequency tuples for observed tokens
        -freqCutoff:            Upper frequency that a token can have and
                                    still be analyzed.
        -bufferSize:            Number of texts to analyze in RAM at one time.
                                    At bufferSize, the current tokenDict is saved
                                    under TEMP_FOLDER_PATH and deleted from RAM.
        -corrNum:               Max number of tokens to include in the ranked
                                    corrList of each token.
        -outPath:               Path to which to save the final corrDict. All
                                    temporary files created during run will
                                    be deleted.
    """

    TEMP_FOLDER_PATH = 'corrDictTablets'

    def corrable(token, freqTuple):
        """ Helper determines if token corr should be taken """
        return False if (freqTuple[0]>freqCutoff) or (False) else True

    # dictionary mapping tokens with frequency below freqCutoff to empty counters
    # aways remains empty as a template for tablets, which will be saved and merged
    emptyTokenDict = {token:Counter() for token, freqTuple in freqDict.items()
                        if corrable(token, freqTuple)}

    def norm_pageTokens(pageTokens):
        """
        Helper normalizes pageToken Counter() by dividing by token frequency
        and cuts those that are below freqCutoff
        """
        return {token : (rawCount / freqDict[token][0]) for token, rawCount
                in pageTokens.items() if token in emptyTokenDict}

    # create temp folder for tablets of tokenDict; delete after merging
    os.mkdir(TEMP_FOLDER_PATH)

    curTokenDict = emptyTokenDict.copy()

    # iterate over each article in filePath
    with open(filePath, 'r') as wikiFile:
        for i, page in enumerate(tqdm(wikiFile)):
            # build counter of token numbers on page and normalize counts by frequency
            pageTokens = Counter(knowledgeProcessor.extract_keywords(page))
            normedTokens = norm_pageTokens(pageTokens)
            # update the related tokens of each token on the page with all the others
            for token in normedTokens.keys():
                if token in tokenDict:
                    curTokenCounter = normedTokens.copy()
                    del curTokenCounter[token]
                    tokenDict[token].update(curTokenCounter)
            # save to temp foldder if at buffer size
            if (i % bufferSize == 0):
                # clean empty tokens from curTokenDict
                cleanTokenDict = {token:counts for token, counts in curTokenDict.items()
                                    if counts.values() != []}
                del curTokenDict
                # save cleaned token dict in temp folder and delete from ram
                save(cleanTokenDict, f'{TEMP_FOLDER_PATH}/tokenDict{i}.sav')
                del cleanTokenDict
                # reinitialize curTokenDict
                curTokenDict = emptyTokenDict.copy()

    # use empty token dict to fold temp tokenDicts together with generator
    for file in os.listdir(TEMP_FOLDER_PATH):
        tokenDict = load(f'{TEMP_FOLDER_PATH}/{file}')
        emptyTokenDict.update(tokenDict)
        del tokenDict

    # minScore is min normed co-occurence score that tokens need to qualify for topTokens
    from math import inf
    minScore = inf

    # build corrDict of top corrNum tokens for each token in tokenDict
    corrDict = {}
    for token, counter in emptyTokenDict.items():
        corrList = [(score, otherToken)
                    for otherToken, score in counter.items()]
        if corrList != []:
            corrList.sort(reverse=True)
            topTokens = [tokenTuple[1] for tokenTuple in corrList[:corrNum]
                            if tokenTuple[1] > minScore]
            corrDict.update({token : topTokens})


    # delete the temporary folder and emptyTokenDict
    os.rmdir(TEMP_FOLDER_PATH)
    del emptyTokenDict

    # save corrDict if prompted
    if outPath:
        save(corrDict, outPath)

    return corrDict




# def build_corr_dict(filePath, knowledgeProcessor, freqDict, freqCutoff=0.0007,
#                     listLength=5, outPath="", readingNum=10000):
#     """
#     Builds dict mapping tokens to the ranked list of tokens with the highest
#     normalized correlation
#     """
#
#     def corrable(token, freqTuple):
#         """ Helper determines if token corr should be taken: NEED TO CHECK IF NUMERIC!!!! """
#         return False if (freqTuple[0]>freqCutoff) or () else True
#
#     # get list of all the tokens in the wiki files as observed in freqDict
#     tokenList = [token for token, freqTuple in freqDict.items()
#                     if corrable(token, freqTuple)]
#
#     # get a list of the counters of each token on each page
#     counterList = []
#     with open(filePath, 'r') as wikiFile:
#         for i, page in enumerate(wikiFile):
#             if i < 10:
#                 counterList.append(Counter(knowledgeProcessor.extract_keywords(page)))
#                 print(f'Building Page Counter List: {i}', end='\r')
#
#     # analyze readingNum tokens at a time until tokenList is empty
#     print('\n')
#     print(tokenList)
#     while tokenList != []:
#         curToken = tokenList.pop(0)
#         print(curToken)
#         curTokenCounter = Counter()
#         print(f'Analyzing Token Correlations. Remaining: {len(tokenList)}')
#         for i, pageCounter in enumerate(counterList):
#             if curToken in pageCounter:
#                 print(pageCounter)
#                 specificCounter = pageCounter.copy()
#                 tokenCount = specificCounter.pop(curToken)
#                 specificCounter = dict(map(lambda token:(specificCounter[token] * tokenCount),
#                                             specificCounter))
#                 curTokenCounter.update(specificCounter)
#                 print(curTokenCounter)
#
#     while tokenList != []:
#         curTokenDict = {token:Counter() for token in tokenList[:readingNum]}
#         tokenList = tokenList[readingNum:]
#         print(f'Analyzing Token Correlations. Remaining: {len(tokenList)}')
#         for pageCounter in enumerate(counterList):
#             for token in curTokenDict:
#                 if token in curTokenDict:
#                     curTokenDict[token].update()
