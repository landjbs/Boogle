"""
Generates set of knowledge tokens, which comprize the keys in the
invertedIndex of the key-val store described in dataStructures.thicctable.
These tokens represent the extent of top-level lookup buckets avaiable to users
and, as such, follow the philosophy of comprehensive concision.
There should be enough knowledge tokens that any reasonable search can be
answered by the contents of a lookup bucket, but not so many as to take up
redundant space.
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


## Knowledge Set Functions ##
def build_knowledgeSet(knowledgeFile, additionalTokens=None, numberRange=None,
                        outPath=None):
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
        assert isinstance(numberRange, tuple), "numberRange must be tuple"
        for num in range(numberRange[0], numberRange[1]):
            knowledgeSet.add(str(num))

    # remove empty token from knowledgeSet (only one because set)
    knowledgeSet.remove("")

    # save knowledge to outPath if specified
    if outPath:
        save(knowledgeSet, outPath)
    return knowledgeSet


### Knowledge Processor Functions ###
def build_knowledgeProcessor(knowledgeSet, outPath=None):
    """ Builds flashtext matcher for words in knowledgeSet iterable """
    # initialize flashtext KeywordProcessor
    knowledgeProcessor = KeywordProcessor(case_sensitive=False)
    # add all items from knowledge set cast as list
    for i, keyword in enumerate(knowledgeSet):
        print(f"\tBuilding knowledgeProcessor: {i}", end="\r")
        knowledgeProcessor.add_keyword(keyword)
    print("\nknowledgeProcessor Built")
    # save knowledgeProcess to outPath if given
    if outPath:
        save(knowledgeProcessor, outPath)
    return knowledgeProcessor

### Freq Dict Functions ###
def fredDict_from_wikiFile(filePath, knowledgeProcessor, outPath=None):
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

    if outPath:
        save(freqDict, outPath)

    return freqDict


def fredDict_from_folderPath(folderPath, knowledgeProcessor, outPath=None):
    """
    Args: folderPath to folder containing files from which to read,
    knowledgeProcessor for token extraction.
    Returns: dict mapping knowledge tokens to tuple of (termFreq, docFreq)
    observed in documents.
        termFreq = (number of times a token is used) / (number of words used)
        docFreq = log ((num of documents) / (num of documents with token))
    """
    # initialize counter to map knowledge tokens to raw number of occurences
    tokenCounts = Counter()
    # initialize counter to map knowledge tokens to number of docs they appear in
    tokenAppearances = Counter()
    # initialize variable to count total number of words used
    totalLength = 0

    # find and iterate over list of files within folderPath
    for i, file in enumerate(os.listdir(folderPath)):
        print(f"\tBuilding freqDict: {i}", end='\r')
        with open(f"{folderPath}/{file}") as FileObj:
            # read in the current file
            text = FileObj.read()
            # find both greedy and subtokens in text
            tokensFound = list(knowledgeFinder.find_rawTokens(text,
                                                            knowledgeProcessor))
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

    if outPath:
        save(freqDict, outPath)

    return freqDict

### Corr Dict Functions ###
def build_corr_dict(filePath, freqDict, freqCutoff=0.0007, bufferSize=40000,
                    corrNum=50, outPath=None):
    """
    Builds dict mapping tokens to the ranked list of corrNum tokens with the
    highest normalized co-occurence in filePath.
    Args:
        -filePath:              Path to the csv file in which the wikipdia
                                    articles are stored
        -freqDict:              Dictionary of freq tuples for observed tokens
        -freqCutoff:            Upper frequency that a token can have and
                                    still be analyzed.
        -bufferSize:            Number of texts to analyze in RAM at one time.
                                    At bufferSize, the current tokenDict is
                                    saved under TEMP_FOLDER_PATH and
                                    deleted from RAM.
        -corrNum:               Max number of tokens to include in the ranked
                                    corrList of each token.
        -outPath:               Path to which to save the final corrDict. All
                                    temporary files created during run will
                                    be deleted.
    Returns:
        Dictionary mapping each qualifying token to a scored and ranked list of
        corrNum relatedTokens with scores as floats in range (0, 1].
    """

    TEMP_FOLDER_PATH = 'corrDictTablets'

    def corrable(token, freqTuple):
        """ Helper determines if token corr should be taken """
        return False if (freqTuple[0]>freqCutoff) or (token.isdigit()) else True

    # dict mapping tokens with frequency below freqCutoff to empty counters
    emptyTokenDict = {token:Counter() for token, freqTuple in freqDict.items()
                        if corrable(token, freqTuple)}

    print(f'{len(emptyTokenDict)} valid tokens found.')

    # build knowledgeProcessor from just tokens to recieve corr scores
    knowledgeProcessor = build_knowledgeProcessor(emptyTokenDict.keys())

    def norm_pageTokens(pageTokens, numWords):
        """
        Helper normalizes pageToken Counter() by dividing by token frequency
        and cuts those that are below freqCutoff
        """
        return {token : ((rawCount / numWords) / freqDict[token][0])
                for token, rawCount in pageTokens.items()}

    # create temp folder for to hold tablets of tokenDict
    safe_make_folder(TEMP_FOLDER_PATH)

    # iterate over each article in filePath
    curTokenDict = {}
    with open(filePath, 'r') as wikiFile:
        for i, page in enumerate(tqdm(wikiFile)):
            # build counter of token nums on page and norm counts by frequency
            pageTokens = Counter(knowledgeProcessor.extract_keywords(page))
            numWords = len(page.split())
            normedTokens = norm_pageTokens(pageTokens, numWords)
            # update the related tokens of each token on the page with others
            for token in normedTokens.keys():
                curTokenCounter = normedTokens.copy()
                curTokenVal = curTokenCounter.pop(token)
                curTokenCounter = Counter({otherToken : round(otherVal)
                                    for otherToken, otherVal
                                    in curTokenCounter.items()})
                if token in curTokenDict:
                    curTokenDict[token].update(curTokenCounter)
                else:
                    curTokenDict.update({token : curTokenCounter})
            # save to temp folder if i is at buffer size
            if (i % bufferSize == 0) and (i > 0):
                # clean empty tokens from curTokenDict
                cleanTokenDict = {token : counts
                                for token, counts in curTokenDict.items()
                                if counts.values() != []}
                # save cleaned token dict in temp folder and delete from RAM
                save(cleanTokenDict, f'{TEMP_FOLDER_PATH}/tokenDict{i}.sav')
                del cleanTokenDict
                # reinitialize curTokenDict
                curTokenDict = {}

    # delete some big objects we won't need to conserve RAM
    del knowledgeProcessor
    del freqDict

    # use last, unsaved curTokenDict as accumulator to fold saved tokenDicts
    print('Folding tokenDict')
    for file in tqdm(os.listdir(TEMP_FOLDER_PATH)):
        try:
            loadedTokenDict = load(f'{TEMP_FOLDER_PATH}/{file}')
            for token, tokenCounter in loadedTokenDict.items():
                if token in curTokenDict:
                    curTokenDict[token].update(tokenCounter)
                else:
                    curTokenDict.update({token : tokenCounter})
            del loadedTokenDict
        except Exception as e:
            print(f'ERROR: {e}')

    def score_to_fraction(tokenTuple, scoreSum):
        """
        Helper converts tokenTuples with rawScores to tokenTuples with
        scores as fractions of topTokens
        """
        return (round((tokenTuple[0] / scoreSum), ndigits=3), tokenTuple[1])


    # build corrDict of top corrNum tokens for each token in tokenDict
    print('Building topTokens')
    corrDict = {}
    for token, counter in tqdm(curTokenDict.items()):
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
    del emptyTokenDict

    # save corrDict if prompted
    if outPath:
        save(corrDict, outPath)

    return corrDict


def vector_update_corrDict(filePath, corrDict, corrWeight=0.6,
                            tokenWeight=0.2, textWeight=0.2, outPath=None):
    """
    Assuming all knowledge tokens are the title of real wikipedia articles
    and that a correlation dict has already been built, adds a layer of scoring
    onto the key-mapped list of (score, token) tuples for each tuple in corrDict
    using (weighted) cosine similarity between BERT vectors of page texts of
    which each token is the title.
    Setup:
        -Run:           bert-serving-start
                            -model_dir /Users/landonsmith/Desktop/shortBert
                            -num_worker=2 -max_seq_len=400
        FIND OUT HOW TO SPAWN AND KILL BERT PROCESSES FROM SCRIPT FOR max_seq_len 400 -> 20
    Args:
        -filePath:      Path to csv of wiki texts
        -corrDict:      Dictionary mapping each token to a scored list of
                            co-occurence tokens created by build_corr_dict
        -corrWeight:    Weight of the co-occurence score of related tokens
        -tokenWeight:   Weight of the vector score of related tokens
        -textWeight:    Weight of the vector score of the descriptive text of
                            related tokens
        -outPath:       Path to which to save the wikiTitle
    Returns:
        Modified corrDict
    """

    weightSum = corrWeight + tokenWeight + textWeight
    assert (weightSum == 1), "Sum of weights must be equal to 1."
    del weightSum

    # uses BERT client with default POOLING_STRATEGRY and MAX_LEN=400
    from bert_serving.client import BertClient
    bc = BertClient(check_length=False)

    def analyze_wiki_line(wikiLine):
        """
        Helper pulls title and text out of a line in the wikiFile csv and
        returns tuple of (cleanTitle, textVec) if the title is a key
        in corrDict
        """
        # get everything after the first comma
        commaLoc = wikiLine.find(',')
        rawText = wikiLine[(commaLoc+2):]
        # pull out the title
        titleEnd = rawText.find('  ')
        title = rawText[:titleEnd]
        cleanTitle = clean_text(title)
        # title is cleaned for checking but text isn't for better vectorization
        if (cleanTitle in corrDict) and (rawText != ''):
            return (cleanTitle, bc.encode([rawText])[0])
        else:
            return None

    print('Vectorizing article texts')
    # iterate over wikiFile texts, vectorizing if title is in corrDict
    with open(filePath, 'r') as wikiFile:
        paraVecList = [analyze_wiki_line(line) for line in tqdm(wikiFile)]

    # convert vec list into dict mapping corrDict tokens to their article's vec
    paraVecDict = {tokenTuple[0] : tokenTuple[1] for tokenTuple
                    in paraVecList if not tokenTuple==None}
    del paraVecList

    print('Vectorizing tokens')
    # build dict mapping tokens in corrDict to their vector
    tokenVecDict = {token : (bc.encode([token])[0])
                        for token in tqdm(corrDict.keys())}


    def score_similarity(relatedToken, relatedScore, baseTokenVec, baseTextVec):
        """
        Helper returns updated score for related token based on vector
        similarity of paragraph and token
        Args:
            relatedToken:   Token from relatedTokens list of baseToken
            relatedScore:   Weighted co-occurence score of relatedToken
                                to baseToken
            baseTokenVec:   Vector of the title of the base token
            baseTextVec:    Vector of the text of the baes token
        Returns:
            scoreTuple:     (updatedScore, relatedToken)
        """
        # score tokens based on vector similarity
        tokenSim =   1 - cosine(baseTokenVec, tokenVecDict[relatedToken])

        # update score with paragraph vec if avaiable; otherwise just boost
        # impact of tokenSim
        if relatedToken in paraVecDict:
            textSim =   1 - cosine(baseTextVec, paraVecDict[relatedToken])
        else:
            textSim = tokenSim

        # create new score aggregating sims by weights and round to 3 digits
        updatedScore = ((corrWeight * relatedScore)
                        + (tokenWeight * tokenSim)
                        + (textWeight * textSim))
        roundedScore = round(updatedScore, ndigits=3)

        return (roundedScore, relatedToken)


    # iterate over corrDict, updating the scores of each token's related tokens
    # by vector similarity
    for baseToken, relatedTokens in corrDict.items():
        if baseToken in paraVecDict:
            # cache vectors of current baseToken
            baseTextVec     =    paraVecDict[baseToken]
            baseTokenVec    =    tokenVecDict[baseToken]
            # update the scores of related tokenDict using helper
            rescoredRelatedTokens = [score_similarity(relatedToken,
                                                        relatedScore,
                                                        baseTokenVec,
                                                        baseTextVec)
                                        for relatedScore, relatedToken
                                        in relatedTokens]
            # rerank relatedTokens according to new scores and update corrDict
            rescoredRelatedTokens.sort(reverse=True)
            corrDict[baseToken] = rescoredRelatedTokens

    # save to outPath if prompted
    if outPath:
        save(corrDict, outPath)

    return corrDict


def build_token_relationships(filePath, freqDict=None, corrWeight=0.6,
                            tokenWeight=0.2, textWeight=0.2, outPath=None):
    """
    Wraps both build_corr_dict and vector_update_corrDict to create dictionary
    mapping each token to a ranked, scored list of related tokens.
    Args:
        -filePath:      Path to csv of wiki texts
        -freqDict:      Dictionary of frequency tuples for observed tokens;
                            will be loaded from memory if none is given
        -corrWeight:    Weight of the co-occurence score of related tokens
        -tokenWeight:   Weight of the vector score of related tokens
        -textWeight:    Weight of the vector score of the descriptive text of
                            related tokens
        -outPath:       Path to which to save the final corrDict
    Returns:
        Dict mapping qualifying tokens from freqDict to a scored and ranked list
        of other qualifying tokens. Related tokens are ranked through three
        mechanisms- co-occurence, synonymity, and descriptive similarity.
        Co-occurence is obtained through build_corr_dict and synonymity
        and descriptive similarity are obtained through vector_update_corrDict.
        Final scores in ranked related token lists are in range (0, 1].
    """

    if not freqDict:
        freqDict = load('data/outData/knowledge/freqDict.sav')

    corrDict = build_corr_dict(filePath=filePath,
                                freqDict=freqDict,
                                corrNum=20,
                                freqCutoff=0.00000001,
                                bufferSize=400,
                                outPath='data/outData/knowledge/corrDict.sav')

    vectoredCorrDict = vector_update_corrDict(filePath=filePath,
                                                corrDict=corrDict,
                                                corrWeight=corrWeight,
                                                tokenWeight=tokenWeight,
                                                textWeight=textWeight,
                                                outPath=outPath)

    return vectoredCorrDict
