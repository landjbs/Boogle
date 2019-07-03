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

import os, re
from flashtext import KeywordProcessor
from collections import Counter
from numpy import log

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
    # knowledgeProcessor.add_keywords_from_list(list(knowledgeSet))
    for i, keyword in enumerate(knowledgeSet):
        print(f"\tBuilding knowledgeProcessor: {i}", end="\r")
        knowledgeProcessor.add_keyword(keyword)
    print("\nknowledgeProcessor Built")
    # save knowledgeProcess to outPath if given
    if not (outPath==""):
        save(knowledgeProcessor, outPath)
    return knowledgeProcessor


def build_freqDict(folderPath, knowledgeProcessor, outPath=""):
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
        if i > 10:
            break
        with open(f"{folderPath}/{file}") as FileObj:
            # read in the current file
            text = FileObj.read()
            # find both greedy and subtokens in text
            tokensFound = list(knowledgeFinder.find_rawTokens(text, knowledgeProcessor))
            # find dict mapping tokens to use number in text
            # curCounts = {token:knowledgeFinder.count_token(token, text) for token in tokensFound}
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
