from os import listdir
from time import time

# from crawlers.crawler import scrape_urlList
# import json
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
from dataStructures.pageObj import Page
from searchers.spellingCorrector import correct

freqDict = load('data/outData/knowledge/freqDict.sav')

print(len(freqDict))


# ### Table initialization ###
print('Loading Knowledge Database')
knowledgeSet = load("data/outData/knowledge/knowledgeSet.sav")
print('Knowledge Database Loaded')
database = Thicctable(knowledgeSet)
del knowledgeSet

# from searchers.searchLexer import topSearch

loadedSet = set()

# Read lists from files into thicctable
for i, file in enumerate(listdir('data/thicctable')):
    if not file in ['DS_Store', 'harvardCrawl']:
        try:
            with open(f'data/thicctable/{file}', 'r', encoding='utf-8') as FileObj:
                pagesList = load(f'data/thicctable/{file}')
                for pageDict in pagesList:
                    pageObj = Page(pageDict)
                    if not pageObj.url in loadedSet:
                        loadedSet.add(pageObj.url)
                        database.bucket_page(pageObj)
        except:
            print(f"ERROR: {file}")
        print(f'Loading Page Files: {i*10}', end='\r')
    else:
        pass

print("Files Loaded")

print('Sorting', end='\r')
database.sort_all()
print('Sorting Complete')

while True:
    search = input('search: ')
    print(database.search_display(search, [search]))

# WORDS = database.all_lengths()

# def flask_search(rawSearch):
#     try:
#         start = time()
#         correctionDisplay, resultList = topSearch(rawSearch, database, WORDS)
#         end = time()
#         searchStats = (len(resultList), round((end - start), 4))
#         return searchStats, correctionDisplay, resultList
#
#     except Exception as e:
#         print(f'ERROR: {e}')
