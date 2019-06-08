import re
import sys, os
import numpy as np
from flashtext import KeywordProcessor
import time

sys.path.append(os.path.abspath(os.path.join('..', '..', 'dataStructures')))
# from dataStructures.objectSaver import save, load
from objectSaver import save, load




if emptyMatcher.fullmatch('a'):
    print('yer')
else:
    print('no')


def clean_knowledgeToken(rawToken):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # lowercase token
    lowerToken = rawToken.lower()
    # replace stripMatcher with "" in lowerToken
    cleanToken = re.sub(stripMatcher, "", lowerToken)
    # replace spaceMathcer with " " in cleanToken
    spaceToken = re.sub(spaceMatcher, " ", cleanToken)
    return spaceToken


def build_knowledgeSet(knowledgeFile, outPath=""):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for strict word search)
    Returns: set (for fast lookup) of tokens stripped from knowledgeData
    """
    # compile matchers for quick matches during iteration
    # matcher for elements to replace with "" in rawToken
    stripString = '[(|)|.|!|?|,|\[|\]|\/|\{|\}|\n|=|$|*|+|"|®|;' + r".\\" + "|']"
    stripMatcher = re.compile(stripString)
    # matcher for elements to convert to spaces
    spaceString = r"[_]"
    spaceMatcher = re.compile(spaceString)
    # matcher for tokens to consider empty: any single character or empty string
    emptyString = r"^(.)?$"
    emptyMatcher = re.compile(emptyString)

    # open file from knowledgeFile path
    with open(knowledgeFile) as knowledgeData:
        # build set of cleaned lines in knowledgeData
        knowledgeSet = {clean_knowledgeToken(token) for token in knowledgeData}
        # knowledgeSet = {cleanToken for token in knowledgeData if (cleanToken := clean_knowledge_token(token)) != ""} ### REPLACE WITH THIS LINE AFTER PYTHON 3.8 COMES OUT !!!! ###p
        # filter out empty tokens from knowledgeSet
        knowledgeSet = set(filter(lambda token : not re.fullmatch(emptyMatcher, token), knowledgeSet))
    # save to outPath if specified
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
        print(f"\t{i}", end="\r")
        knowledgeProcessor.add_keyword(keyword)
    print("\nknowledgeProcessor Built")
    if not (outPath==""):
        save(knowledgeProcessor, outPath)
    return knowledgeProcessor

def find_knowledgeTokens(pageText, knowledgeProcessor):
    """ Returns dict mapping knowledge tokens found in text to number of occurences """
    # use knowledgeProcessor to extract tokens from page text
    keywordsFound = knowledgeProcessor.extract_keywords(pageText)
    # create dict mapping keywords to number of times used in pageText using re.findall()
    keywordDict = {keyword:(len(re.findall(keyword, pageText))) for keyword in keywordsFound}
    return keywordDict







# ### TESTING ###
# knowledgeSet = build_knowledgeSet("enwiki-latest-all-titles-in-ns0",
#                     outPath="/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")

# knowledgeList = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))
#
# print(knowledgeList[:200])
#
# knowledgeProcessor = build_knowledgeProcessor(knowledgeList[:200], "test")
# # print("Created")
#
# while True:
#     test = input("Search: ")
#     test = clean_knowledgeToken(test)
#     out = find_knowledgeTokens(test, knowledgeProcessor)
#     print(out)













pass
