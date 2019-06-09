import sys, os

# sys.path.append(os.path.abspath(os.path.join('..', '..')))

import urllib.request
from models.knowledge.knowledgeTokenizer import build_knowledgeProcessor, find_knowledgeTokens
import crawlers.htmlAnalyzer as ha
from dataStructures.objectSaver import save, load
import time


while True:
    test = input("Search: ")
    x = ha.scrape_url(test)
    print(x)


# print(time.time())
#
# start = time.time()
# knowledgeProcessor = load('/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend/data/outData/knowledgeProcessor.match')
# end = time.time()
#
# print(f"Time: {end - start}")
#
#
# while True:
#     url = input("URL: ")
#     try:
#         pageString = url_to_pageString(url)
#         pageInfo = ha.analyze_html(pageString)
#         title = pageInfo['title']
#         print(title)
#         print(find_knowledgeTokens(title, knowledgeProcessor))
#     except Exception as e:
#         print(e)
