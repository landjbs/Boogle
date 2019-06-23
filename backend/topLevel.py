from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
from models.processing.cleaner import clean_text
from crawlers.crawler import scrape_urlList
from os import listdir
import json
from searchers.databaseSearcher import search_database
from dataStructures.pageObj import Page
import time

### url Reading ###
# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[3000:40000]))
# scrape_urlList(urlList)


# ### Table initialization ###
print('Loading Knowledge Database')
knowledgeSet = load("data/outData/knowledge/knowledgeSet.sav")
print('Knowledge Database Loaded')
database = Thicctable(knowledgeSet)
del knowledgeSet

from searchers.searchLexer import topSearch

# Read lists from files into thicctable
for i, file in enumerate(os.listdir('data/thicctable/tempLists')):
    if not file=='.DS_Store':
        with open(f'data/thicctable/tempLists/{file}', 'r', encoding='utf-8') as FileObj:
            tempList = json.loads(FileObj.read())
            for pageList in tempList:
                pageObj = Page(pageList)
                database.bucket_page(pageObj)
        print(f'Loading Page Files: {i*10}', end='\r')
    else:
        pass
print("Files Loaded")

database.sort_all()


print(f"\n{'-'*73}\nWelcome to Boogle\t\t\t\t\t\t\t|\n{'-'*73}")
while True:
    try:
        rawSearch = input("Search: ")

        start = time.time()
        correctionDisplay, resultList = topSearch(rawSearch, database)
        end = time.time()

        resultString = f"<u><strong>BOOGLE SEARCH</strong></u><br><i>{len(resultList)} results returned in {round(end-start, 3)} seconds!</i><br>"

        # inform the user if a correction was made
        if correctionDisplay != None:
            resultString += f"Showing results for <u>{correctionDisplay}.</u><br>"

        resultString += "<br><ul>"
        # iterate through the results, adding each page to the <ul>
        for i, result in enumerate(resultList[:20]):
            url, title, windowText = result
            resultString += f"<li><u><strong>{title}</strong></u><br><i>{url}</i><br>{windowText}</li>"
        resultString += "</ul>"
        print(resultString)

    except Exception as e:
        print(f'ERROR: {e}')
