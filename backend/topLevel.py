from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
from crawlers.crawler import scrape_urlList
from os import listdir
import json
from dataStructures.pageObj import Page
import time
from searchers.spellingCorrector import correct

### url Reading ###
# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[1000:40000]))
# scrape_urlList(urlList)

# ### Table initialization ###
print('Loading Knowledge Database')
knowledgeSet = load("backend/data/outData/knowledge/knowledgeSet.sav")
print('Knowledge Database Loaded')
database = Thicctable(knowledgeSet)
del knowledgeSet

from searchers.searchLexer import topSearch

loadedSet = set()

# Read lists from files into thicctable
for i, file in enumerate(listdir('backend/data/thicctable/627amCrawl')):
    if not file=='.DS_Store':
        with open(f'backend/data/thicctable/627amCrawl/{file}', 'r', encoding='utf-8') as FileObj:
            tempList = json.loads(FileObj.read())
            for pageList in tempList:
                pageObj = Page(pageList)
                if not pageObj.url in loadedSet:
                    loadedSet.add(pageObj.url)
                    database.bucket_page(pageObj)
        print(f'Loading Page Files: {i*10}', end='\r')
    else:
        pass

print("Files Loaded")

print('Sorting', end='\r')
database.sort_all()
print('Sorting Complete')

WORDS = database.all_lengths()

def flask_search(rawSearch):
    try:
        start = time.time()
        correctionDisplay, resultList = topSearch(rawSearch, database, WORDS)
        end = time.time()
        searchStats = (len(resultList), round((end - start), 4))
        return searchStats, correctionDisplay, resultList

    except Exception as e:
        print(f'ERROR: {e}')
