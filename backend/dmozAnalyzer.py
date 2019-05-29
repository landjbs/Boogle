import re
import pandas as pd
import crawlers.urlAnalyzer as ua
from queue import Queue
from threading import Thread

import time

dmozDF = pd.read_csv("data/test.tab.tsv", sep="\t", names=["url", "path"])

dmoz_urlList = list(dmozDF["url"])

# globals for modification during scraping
dmoz_pageStrings = []
errors = 0

#### URL QUEUE STUFF ####
url_queue = Queue(10)

def worker():
    """ Worker to process pop url from url_queue """
    # set globals
    global dmoz_pageStrings
    global errors
    while True:
        url = url_queue.get()
        try:
            pageString = ua.url_to_string(url)
            dmoz_pageStrings.append(pageString)
        except:
            errors += 1
        url_queue.task_done()

for i in range(20):
    t = Thread(target=worker)
    t.daemon = True
    t.start()

start = time.time()

for count, url in enumerate(dmoz_urlList):
    print(f"\t{count} URLs analyzed with {errors} errors!", end="\r")
    url_queue.put(url)

end = time.time()

print(f"Time: {end - start}")

url_queue.join()

dmozDF["pageString"] = dmoz_pageStrings

dmozDF.to_csv("data/dmoz.tab.tsv", sep='\t')
