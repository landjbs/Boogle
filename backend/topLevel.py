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
    for token in knowledgeDict:
        score = knowledgeDict[token]
        pageList.append((1000/score))
        pageTuple = tuple(pageList)
        try:
            testData.insert_value(token, pageTuple)
            testData.sort_key(token, index=-1)
            print(f'\tPage Added to {token}', end='\r')
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

save(testData, 'thiccTest')

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


# print(time.time())
#
# start = time.time()
# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# end = time.time()
#
# print(f"Time: {end - start}")
#
#
# while True:
#     url = input("URL: ")
#     try:
#         pageString = url_to_pageString(url)
#         pageInfo = ha.analyze_html(pageString)
#         title = pageInfo['title']
#         print(title)
#         print(find_knowledgeTokens(title, knowledgeProcessor))
#     except Exception as e:
#         print(e)
