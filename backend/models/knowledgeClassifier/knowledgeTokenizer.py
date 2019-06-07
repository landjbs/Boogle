import re
import sys, os

import time

sys.path.append(os.path.abspath(os.path.join('..', '..', 'dataStructures')))
from objectSaver import save, load

# matcher for elements to replace with "" in rawToken
stripString = '[(|)|.|!|?|,|\[|\]|\/|\{|\}|\n|=|$|*|+|"' + r".\\" + "|']"
stripMatcher = re.compile(stripString)

# matcher for elements to convert to spaces
spaceString = "[-]"
spaceMatcher = re.compile(spaceString)


def clean_knowledge_token(rawToken):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # lowercase token
    lowerToken = rawToken.lower()
    # replace stripMatcher with "" in lowerToken
    cleanToken = re.sub(stripMatcher, "", rawToken)
    # replace spaceMathcer with " " in cleanToken
    spaceToken = re.sub(spaceMatcher, " ", rawToken)
    return spaceToken


def build_knowledgeSet(knowledgeFile, outPath=""):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for strict word search)
    Returns: set (for fast lookup) of tokens stripped from knowledgeData
    """

    with open(knowledgeFile) as knowledgeData:
        # build set of cleaned lines in knowledgeData
        knowledgeSet = {clean_knowledge_token(token) for token in knowledgeData}
        # knowledgeSet = {cleanToken for token in knowledgeData if (cleanToken := clean_knowledge_token(token)) != ""} ### REPLACE WITH THIS LINE AFTER PYTHON 3.8 COMES OUT !!!! ###
        # filter out empty tokens from knowledgeSet
        knowledgeSet = set(filter(lambda token : (token != ""), knowledgeSet))
        print(f"Time: {end - start}")
    if not (outPath==""):
        save(knowledgeSet, outPath)
    return knowledgeSet

def build_knowledgeMatcher(knowledgeSet, outPath=""):
    """ Builds regex matcher for words in knowledgeSet """
    knowledgeString = "(?" + "|".join(knowledgeSet) + ")"
    print(knowledgeString)
    knowledgeMatcher = re.compile(knowledgeString)
    if not (outPath==""):
        save(knowledgeMatcher, outPath)
    return knowledgeString

def knowledgeTokenize_search(inStr, knowledgeSet):
    """ Checks if inStr is in knowledgeSet. TO IMPROVE!!!!!!!! """
    if (inStr in knowledgeSet):
        return inStr


knowledgeSet = build_knowledgeSet("enwiki-latest-all-titles-in-ns0",
                    outPath="/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")

print('Built')

# knowledgeSet = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set')

# knowledgeMatcher = build_knowledgeMatcher(knowledgeSet[:2000], outPath="/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeMatcher.re")
# print("Created")
#


# print(knowledgeMatcher)
# knowledgeMatcher = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeMatcher.re')

# print(knowledgeMatcher)
#
while True:
    test = input("Search: ")
    test = clean_knowledge_token(test)
    for token in knowledgeSet:
        curToken = test.find(token)
        if not curToken==-1:
            print(curToken)













pass
