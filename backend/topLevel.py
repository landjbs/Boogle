from time import time

from crawlers.crawlLoader import load_crawled_pages

database, uniqueWords, searchProcessor = load_crawled_pages('data/thicctable/wikiCrawl')

# def flask_search(rawSearch):
#     try:
#         start = time()
#         correctionDisplay, resultList = topSearch(rawSearch, database, WORDS)
#         end = time()
#         searchStats = (len(resultList), round((end - start), 4))
#         return searchStats, correctionDisplay, resultList
#
#     except Exception as e:
#         print(f'ERROR: {e}')
