import sys, os

sys.path.append(os.path.abspath(os.path.join('..', '..')))

import urllib.request
from models.knowledgeClassifier.knowledgeTokenizer import build_knowledgeProcessor, find_knowledgeTokens
from crawlers.urlAnalyzer import url_to_pageString
import crawlers.htmlAnalyzer as ha

from dataStructures.objectSaver import save, load
import time

print(time.time())

start = time.time()
knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
end = time.time()

print(f"Time: {end - start}")


while True:
    url = input("URL: ")
    try:
        pageString = url_to_pageString(url)
        pageInfo = ha.analyze_html(pageString)
        title = pageInfo['title']
        print(title)
        print(find_knowledgeTokens(title, knowledgeProcessor))
    except Exception as e:
        print(e)
