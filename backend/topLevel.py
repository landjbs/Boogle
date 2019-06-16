import models.knowledge.knowledgeFinder as knowledgeFinder
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
import models.binning.docVecs as docVecs
import crawlers.htmlAnalyzer as htmlAnalyzer
from models.processing.cleaner import clean_text
from crawlers.crawler import scrape_urlList
import json
import os

### url Reading ###
# urlList = list(map(lambda url:(url[:-4]), os.listdir('data/outData/dmozProcessed/All')[13000:20000]))
#
# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
# print("Processor loaded")
#
# scrape_urlList(urlList, knowledgeProcessor)



### Table initialization ###
knowledgeSet = load("data/outData/knowledge/knowledgeSet.sav")
database = Thicctable(knowledgeSet)
del knowledgeSet


dataList = []
# Read lists from files into thicctable
for file in os.listdir('data/thicctable/tempLists'):
    with open(f'data/thicctable/tempLists/{file}', 'r') as FileObj:
        tempList = json.loads(FileObj.read())
        for pageList in tempList:
            database.bucket_page(pageList)


searchLambda = lambda item : item[:2]

knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
print("Processor loaded")

print(f"\n{'-'*73}\nWelcome to Boogle\t\t\t\t\t\t\t|\n{'-'*73}")
while True:
    try:
        search = input("Search: ")
        clean_search = clean_text(search)
        searchList = knowledgeFinder.find_rawTokens(clean_search, knowledgeProcessor)
        resultsList = [database.search_index(token, searchLambda, n=10000) for token in searchList]
        showList = [result for result in resultsList[0] if all((result in other) for other in resultsList[1:])]
        for i, result in enumerate(showList[:20]):
            print(f"\t\t{i}: {result}")
        print('\r')
    except Exception as e:
        print(f'ERROR: {e}')
