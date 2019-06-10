# crawlers
import crawlers.htmlAnalyzer as ha
# data structures
from dataStructures.thicctable import Thicctable
from dataStructures.objectSaver import load, save
# models
from models.knowledge.knowledgeTokenizer import build_knowledgeProcessor
from models.processing.cleaner import clean_text

import re

# knowledgeSet load
knowledgeSet = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))
testData = Thicctable(knowledgeSet)

print('Data Table Created')

# del knowledgeSet

# load knowledgeProcessor
knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
print('Knowledge Processor Created')


def bin_page(pageList):
    """ Test function to pull out and score dict from tuple """
    knowledgeDict = pageList[2]
    print("Adding Page to:", end=" ")
    for token in knowledgeDict:
        score = knowledgeDict[token]
        pageList.append((1000/score))
        pageTuple = tuple(pageList)
        try:
            testData.insert_value(token, pageTuple)
            testData.sort_key(token, index=-1)
            print(f'{token}', end=' | ')
        except Exception as e:
            print(e)

urlMatcher = re.compile('(?<=").+(?="\t)')

# load webpages
with open('data/inData/test.tab.tsv') as dmozData:
    for i, line in enumerate(dmozData):
        try:
            url = urlMatcher.findall(line)[0]
            print(url)
            pageList = ha.scrape_url(url, knowledgeProcessor)
            bin_page(pageList)
            print(f"Analyzing: {i}")
        except Exception as e:
            print(f"ERROR: {e}")

save(testData.topDict, 'thiccTest')

# BOOGLE #
print(f"{'-'*40}\nWelcome to Boogle!\n{'-'*40}")
while True:
    try:
        rawSearch = input("Search: ")
        cleanSearch = clean_text(rawSearch)
        print(cleanSearch)
        print(f"\t\t\t\tSearch Results:\n\t\t\t\t{testData.search_index(cleanSearch, indexLambda=(lambda x: x[:2]))}")
    except Exception as e:
        print(f"\t\tERROR: {e}")


## MANUAL ENTRY ##
# print(f"{'-'*40}\nWelcome to Boogle!\n{'-'*40}")
# while True:
#     try:
#         action = int(input("1 - Add Page; 2 - Search\nAction: "))
#         assert (action in [1,2]), "Action must be 1 or 2"
#         if (action==1):
#             url = input("Page URL: ")
#             pageList = ha.scrape_url(url, knowledgeProcessor)
#             bin_page(pageList)
#         else:
#             rawSearch = input("Search: ")
#             cleanSearch = clean_text(rawSearch)
#             print(cleanSearch)
#             print(f"\t\t\t\tSearch Results:\n\t\t\t\t{testData.search_index(cleanSearch, indexLambda=(lambda x: x[:1]))}")
#     except Exception as e:
#         print(f"\t\tERROR: {e}")
