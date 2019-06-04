import re
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '..', 'dataStructures')))
from objectSaver import save, load

# matcher for elements to replace with "" in rawToken
stripString = r"[(|)|\n|\t]"
stripMatcher = re.compile(stripString)

# matcher for elements to replace with " " in rawToken
spaceString = r"_"
spaceMatcher = re.compile(spaceString)


def clean_knowledge_token(rawToken):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # replace stripMatcher with "" in rawToken
    cleanToken = re.sub(stripMatcher, "", rawToken)
    # replace spaceMatcher with " " in cleanToken
    spacedToken = re.sub(spaceMatcher, " ", cleanToken)
    # lowercase token
    lowerToken = spacedToken.lower()
    return lowerToken


def build_knowledgeSet(knowledgeFile, outPath):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for strict word search)
    Returns: set (for fast lookup) of tokens stripped from knowledgeData
    """
    with open(knowledgeFile) as knowledgeData:
        knowledgeSet = {clean_knowledge_token(token) for token in knowledgeData}
    if not (outPath==""):
        save(knowledgeSet, outPath)
    return knowledgeSet

def get_knowledgeTokens(inStr, knowledgeSet):
    """ Scans all possible combinations """
    if (inStr in knowledgeSet):
        print(inStr)

build_knowledgeSet("enwiki-latest-all-titles-in-ns0", outPath="knowledgeTokens.set")


x = load("knowledgeTokens.set")

while True:
    search = input("Search: ")
    get_knowledgeTokens(search, x)





















pass
