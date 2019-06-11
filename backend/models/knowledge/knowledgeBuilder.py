"""
Generates set of knowledge tokens, which comprize the keys in the topDict of
the key-val store described in dataStructures.thicctable. These tokens
represent the extent of top-level lookup buckets avaiable to users and, as
such, follow the philosophy of comprehensive concision. There should be enough
knowledge tokens that any reasonable search can be answered by the contents of
a lookup bucket, but not so many as to take up redundant space.
Knowledge tokens are only permitted to be words and phrases; tokens comprised
soley of non-alpha chars will be mapped to the English representation of the
token (eg. & -> ampersand)
"""

from dataStructures.objectSaver import save, load
from models.processing.cleaner import clean_text


## Functions ##
def build_knowledgeSet(knowledgeFile, outPath=""):
    """
    Args: \n delimited file of words to treat as knowledge tokens (tokens for
    strict word search).
    Returns: set (for fast lookup) of cleaned tokens stripped from knowledgeData
    """
    # open file from knowledge
    with open(knowledgeFile) as knowledgeData:
        # build set of cleaned lines in knowledgeData
        knowledgeSet = {clean_text(token) for token in knowledgeData}
        # remove empty token from knowledgeSet (only one because set)
        knowledgeSet.remove("")
    # save knowledge to outPath if specified
    if not (outPath==""):
        save(knowledgeSet, outPath)
    return knowledgeSet

# knowledgeList = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))


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

# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# knowledgeProcessor = build_knowledgeProcessor(knowledgeList)

def find_knowledgeTokens(pageText, knowledgeProcessor):
    """
    Returns dict mapping knowledge tokens found in text to number of occurences
    """
    # use knowledgeProcessor to extract tokens from page text
    keywordsFound = knowledgeProcessor.extract_keywords(pageText)
    # create dict mapping keywords to number of times used in pageText using re.findall()
    keywordDict = {keyword:(len(re.findall(keyword, pageText, re.IGNORECASE))) for keyword in keywordsFound}
    return keywordDict









pass
