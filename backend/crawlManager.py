from os import listdir

# from crawlers.crawler import scrape_urlList
from crawlers.htmlAnalyzer import scrape_url

from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from dataStructures.objectSaver import load

knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
freqDict = load('data/outData/knowledge/freqDict.sav')


# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[1000:40000]))
