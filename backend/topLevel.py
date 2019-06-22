import models.knowledge.knowledgeFinder as knowledgeFinder
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
# import models.binning.docVecs as docVecs
import crawlers.htmlAnalyzer as htmlAnalyzer
from models.processing.cleaner import clean_text
from crawlers.crawler import scrape_urlList
import json
import os
from searchers.databaseSearcher import search_database
from crawlers.urlAnalyzer import parsable
from dataStructures.pageObj import Page

### url Reading ###
urlList = list(map(lambda url:(url[:-4]), os.listdir('data/outData/dmozProcessed/All')[0:10]))

scrape_urlList(urlList)

### Table initialization ###
print('Loading Knowledge Database')
knowledgeSet = load("data/outData/knowledge/knowledgeSet.sav")
print('Knowledge Database Loaded')
database = Thicctable(knowledgeSet)
del knowledgeSet

# Read lists from files into thicctable
print('Loading Page Files')
for i, file in enumerate(os.listdir('data/thicctable/tempLists')):
    with open(f'data/thicctable/tempLists/{file}', 'r', encoding='utf-8') as FileObj:
        tempList = json.loads(FileObj.read())
        for pageList in tempList:
            pageObj = Page(pageList[0], pageList[1], pageList[2], pageList[3], pageList[4], pageList[5], pageList[6], pageList[7])
            database.bucket_page(pageList)
    print(f"Loading: {i*500}")
print("Files Loaded")

searchLambda = lambda item : item[:2]

print('Loading Knowledge Processor')
knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
print("Processor loaded")

print(f"\n{'-'*73}\nWelcome to Boogle\t\t\t\t\t\t\t|\n{'-'*73}")
while True:
    try:
        rawSearch = input("Search: ")
        if rawSearch=="OS.CLEAR":
            os.system('clear')
        else:
            resultList = search_database(rawSearch, knowledgeProcessor, database)
            ## Old but different ##
            # clean_search = clean_text(search)
            # searchList = knowledgeFinder.find_rawTokens(clean_search, knowledgeProcessor)
            # resultsList = [database.search_index(token, searchLambda, n=10000) for token in searchList]
            # showList = [result for result in resultsList[0] if all((result in other) for other in resultsList[1:])]
            for i, result in enumerate(resultList):
                print(f"\t\t{i}: {result}")
            print('\r')
    except Exception as e:
        print(f'ERROR: {e}')
