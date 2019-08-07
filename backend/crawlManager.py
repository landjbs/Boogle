# from crawlers.wikiCrawler import crawl_wiki_data
# from dataStructures.objectSaver import load
# from models.knowledge.knowledgeBuilder import build_corr_dict, build_knowledgeProcessor

# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[345:1000]))
# scrape_urlList(urlList)

### wiki stuff ###
# knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
# freqDict = fredDict_from_wikiFile('data/inData/wikipedia_utf8_filtered_20pageviews.csv', knowledgeProcessor, "data/outData/knowledge/freqDict.sav")

# for o in dir():
#     if not o in ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'crawl_wiki_data']:
#         del o
#
# print([elt for elt in dir()])

crawl_wiki_data(inPath='data/inData/wikipedia_utf8_filtered_20pageviews.csv',
                outPath='data/thicctable/wikiCrawl4',
                startNum=0,
                endNum=None)
