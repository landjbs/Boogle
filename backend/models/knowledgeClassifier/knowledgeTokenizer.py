import re
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '..', 'dataStructures')))
from objectSaver import save, load

# matcher for elements to replace with "" in rawToken
stripString = '[(|)|.|!|?|\[|\]|\{|\}|\n|=|$|*|+|"|' + r"\\" + "|']"
stripMatcher = re.compile(stripString)

# matcher for elements to replace with "_" in rawToken
conversionString = "[-| ]"
conversionMatcher = re.compile(conversionString)


def clean_knowledge_token(rawToken):
    """ Cleans rawToken by stripping parentheses and replacing _ with spaces """
    # replace stripMatcher with "" in rawToken
    cleanToken = re.sub(stripMatcher, "", rawToken)
    # replace conversionMatcher with "_" in in cleanToken
    convertedToken = re.sub(conversionMatcher, "_", cleanToken)
    # lowercase token
    lowerToken = convertedToken.lower()
    print(f"Before: {rawToken} | After: {lowerToken}")
    return lowerToken


def build_knowledgeSet(knowledgeFile, outPath=""):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for strict word search)
    Returns: set (for fast lookup) of tokens stripped from knowledgeData
    """
    with open(knowledgeFile) as knowledgeData:
        # knowledgeSet = {clean_knowledge_token(token) for token in knowledgeData}
        knowledgeSet = [clean_knowledge_token(token) for token in knowledgeData]
        knowledgeSet = list(filter(lambda token : (token !=""), knowledgeSet))
    if not (outPath==""):
        save(knowledgeSet, outPath)
    return knowledgeSet

def build_knowledgeMatcher(knowledgeSet, outPath=""):
    """ Builds regex matcher for words in knowledgeSet """
    knowledgeString = "(" + "|".join(knowledgeSet) + ")"
    knowledgeMatcher = re.compile(knowledgeString)
    if not (outPath==""):
        save(knowledgeMatcher, outPath)
    return knowledgeString

def knowledgeTokenize_search(inStr, knowledgeSet):
    """ Checks if inStr is in knowledgeSet. TO IMPROVE!!!!!!!! """
    if (inStr in knowledgeSet):
        return inStr


# print(clean_knowledge_token("1\2Python-docs\n"))


# knowledgeSet = build_knowledgeSet("enwiki-latest-all-titles-in-ns0",
#                     outPath="/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set")

# print('Built')

knowledgeSet = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set')

# knowledgeMatcher = build_knowledgeMatcher(knowledgeSet[:2000], outPath="/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeMatcher.re")
# print("Created")
#

knowledgeMatcher = build_knowledgeMatcher([clean_knowledge_token(token) for token in ["hi", "hi college","h", "hyo"]])

print(knowledgeMatcher)
# knowledgeMatcher = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeMatcher.re')

# print(knowledgeMatcher)
#
while True:
    test = input("Search: ")
    test = clean_knowledge_token(test)
    print(re.findall(knowledgeMatcher, test))













pass
