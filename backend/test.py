from crawlers.crawler import scrape_urlList
from os import listdir

urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[3000:40000]))

scrape_urlList(urlList)
