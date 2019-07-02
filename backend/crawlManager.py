from os import listdir

# from crawlers.crawler import scrape_urlList
from crawlers.htmlAnalyzer import scrape_url

from models.knowledge.knowledgeBuilder import build_knowledgeProcessor

from dataStructures.thicctable import Thicctable
from dataStructures.pageObj import Page
from dataStructures.objectSaver import load

# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[1000:40000]))
urlList = ['https://www.harvard.edu', 'https://twitter.com/Harvard?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor',
            'https://en.wikipedia.org/wiki/Harvard_University', 'https://www.hbs.edu',
            'https://www.thecrimson.com', 'http://www.harvard.com']


# knowledgeSet = load('data/outData/knowledge/knowledgeSet.sav')
knowledgeSet = {'harvard'}
print('set')
# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
knowledgeProcessor = build_knowledgeProcessor(knowledgeSet)
print('processor')

database = Thicctable(knowledgeSet)

for i, url in enumerate(urlList):
    try:
        print(url)
        pageList = scrape_url(url=url, knowledgeProcessor=knowledgeProcessor, freqDict={})
        pageObj = Page(pageList)
        database.bucket_page(pageObj)
    except Exception as e:
        print(f'\tERROR: {e}')
    print(f'Scraping {i}')


while True:
    search = input('search: ')
    try:
        results = database.search_display(search, [search])
        for result in results:
            print(f"\t{result[0]}\n\t{result[1]}\n\t{result[2]}\n\n")
    except:
        pass
