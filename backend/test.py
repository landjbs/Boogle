import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '..', 'dataStructures')))
sys.path.append(os.path.abspath(os.path.join('..', '..', 'crawlers')))

import urllib.request
from models.knowledgeClassifier.knowledgeTokenizer import build_knowledgeProcessor, find_knowledgeTokens
from crawlers.urlAnalyzer import url_to_pageString
from crawlers.htmlAnalyzer import get_pageText

from dataStructures.objectSaver import save, load


knowledgeList = list(load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeTokens.set'))
knowledgeProcessor = build_knowledgeProcessor(knowledgeList)

while True:
    url = input("URL: ")
    try:
        pageString = url_to_pageString(url)
        pageText = get_pageText(pageString)
        print(find_knowledgeTokens(pageText, knowledgeProcessor))
    except:
        print(f"Error Accessing {url}")
