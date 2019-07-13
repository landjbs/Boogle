from os import listdir

from crawlers.wikiCrawler import crawl_wiki_data

# urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[345:1000]))
# scrape_urlList(urlList)

crawl_wiki_data('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'data/thicctable/wikiCrawl')
