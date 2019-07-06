from os import listdir

from crawlers.crawler import scrape_urlList

urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[0:20]))

scrape_urlList(urlList)
