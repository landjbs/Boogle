import models.knowledge.knowledgeFinder as knowledgeFinder
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.objectSaver import load
from dataStructures.thicctable import Thicctable
import models.binning.docVecs as docVecs
import crawlers.htmlAnalyzer as htmlAnalyzer
from models.processing.cleaner import clean_text
from crawlers.crawler import scrape_urlList

import os

# urlList = list(map(lambda url:url[:-4], os.listdir('data/outData/dmozProcessed/All')[1000:2000]))

urlList = ['https://www.harvard.edu', 'https://en.wikipedia.org/wiki/Harvard_University',
            'https://en.wikipedia.org/wiki/Harvard_College', 'https://www.espn.com/college-football/game?gameId=401029858',
            'https://en.wikipedia.org/wiki/Dartmouth–Harvard_football_rivalry']

knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
print("Processor loaded")

database = scrape_urlList(urlList, knowledgeProcessor)

database.sort_all()

searchLambda = lambda item : item[:2]

print(f"\n{'-'*73}\nWelcome to Boogle\t\t\t\t\t\t\t|\n{'-'*73}")
while True:
    try:
        search = input("Search: ")
        clean_search = clean_text(search)
        searchList = knowledgeFinder.find_rawTokens(clean_search, knowledgeProcessor)
        for token in searchList:
            results = database.search_index(token, searchLambda)
            print(f"\t{token} Results:")
            for i, elt in enumerate(results):
                print(f"\t\t{i}: {elt}")

    except Exception as e:
        print(f'ERROR: {e}')
