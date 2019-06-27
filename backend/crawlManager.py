from os import listdir

from crawlers.crawler import scrape_urlList

print('test')
urlList = list(map(lambda url:(url[:-4]), listdir('data/outData/dmozProcessed/All')[1000:40000]))
print('ready')
scrape_urlList(urlList)
