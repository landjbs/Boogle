from crawlers.htmlAnalyzer import scrape_url
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from dataStructures.thicctable import Thicctable
from dataStructures.pageObj import Page

knowledgeSet = {'harvard', 'college', 'university', 'study', 'john'}

knowledgeProcessor = build_knowledgeProcessor(knowledgeSet)

freqDict = {}
d2vModel = {}

database = Thicctable(knowledgeSet)

urlList = ['www.harvard.edu', 'https://en.wikipedia.org/wiki/Harvard_University']

for url in urlList:
    try:
        pageList = scrape_url(url, knowledgeProcessor, freqDict, d2vModel)
        pageObj = Page(pageList)
        database.bucket_page(pageObj)
    except:
        pass

database.sort_all()

print(database.topDict)

while True:
    try:
        search = input('search: ')
        resultList = database.search_full(search)
        for elt in resultList:
            print(f"{elt[1].url}\n\tScore: {elt[0]}, Load time: {elt[1].loadTime}")
    except Exception as e:
        print(e)
