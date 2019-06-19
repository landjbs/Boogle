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
from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text


## Functions ##
def build_knowledgeSet(knowledgeFile, additionalTokens=None, numberRange=None, outPath=""):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for
    strict word search), additionalTokens set of tokens not in knowledgeFile,
    numberRange tuple of range of integer tokens to add, and outPath to which to save set.
    Returns: set (for fast lookup) of cleaned tokens stripped from knowledgeData
    """
    # open file from knowledge
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


def count_token(token, pageText):
    """
    Uses regexp to return number of times a token is used in pageText.
    Matches for tokens that are not parts of larger, uninterrupted words.
    Does not require a knowledgeProcessor.
    """
    return len(re.findall(f"(?<![a-zA-Z]){token}(?![a-zA-Z])", pageText, flags=re.IGNORECASE))


def build_freqDict(folderPath, knowledgeProcessor, outPath=""):
    """
    Args: folderPath to folder containing files from which to read,
    knowledgeProcessor for token extraction.
    Returns: dict mapping knowledge tokens to average frequency of occurence in
    files. Only tokens found in files will have associated frequency.
    """
    # initialize dict to store sum of frequencies and number of with token
    rawDict = {}
    # find and iterate over list of files within folderPath
    files = os.listdir(folderPath)
    for i, file in enumerate(files):
        print(f"\t{i}", end='\r')
        if i > 1000:
            break
        with open(f"{folderPath}/{file}") as FileObj:
            # read in the current file
            text = FileObj.read()
            # find number of words in the current file
            textLen = len(text.split())
            # find tokens in the current file
            tokensFound = set(knowledgeProcessor.extract_keywords(text))
            # iterate over tokensFound
            for token in tokensFound:
                # find number of occurences of token in current file
                tokenNum = count_token(token,text)
                # find frequency of token use in current file
                tokenFreq = tokenNum / textLen
                # check if token has been seen before
                if not token in rawDict:
                    # if not seen before, add token map to current freq and one occurence
                    rawDict.update({token:[tokenFreq, 1]})
                else:
                    # if see before, add current freq to first elt of token map and increment number occurences
                    rawDict[token][0] += tokenFreq
                    rawDict[token][1] += 1
    # lambda to normalize tokenFreq by number of pages
    normalizeFreq = lambda val : val[0] / val[1]
    # create normalized freqDict
    freqDict = {token:normalizeFreq(rawDict[token]) for token in rawDict}
    if (outPath != ""):
        save(freqDict, outPath)
    return freqDict

















pass
