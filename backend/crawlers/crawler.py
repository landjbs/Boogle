"""
Responsible for building database of page data from list of URLs.
Outsources URL processing to urlAnalyzer.py
Outsources HTML processing to htmlAnalyzer.py
Outsoucres database definitions to thicctable.py
"""

from queue import Queue
from threading import Thread
from time import time
from termcolor import colored

from crawlers.urlAnalyzer import fix_url
from crawlers.htmlAnalyzer import scrape_url
from dataStructures.scrapingStructures import Simple_List, Metrics
from dataStructures.objectSaver import save, load
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor


def scrape_urlList(urlList, runTime=100000000, queueDepth=1000000, workerNum=2):
    """
    Rescursively crawls internet from starting urlList and ends after runTime
    seconds.
    """

    # load models and datasets
    print(colored('Loading freqDict', color='red'), end='\r')
    freqDict = load('data/outData/knowledge/freqDict.sav')
    print(colored('Complete: Loading freqDict', color='cyan'))

    print(colored('Loading knowledgeProcessor', color='red'), end='\r')
    knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
    print(colored('Complete: Loading knowledgeProcessor', color='cyan'))

    # queue to hold urlList
    urlQueue = Queue(queueDepth)
    # set to hold , previously scraped URLs
    scrapedUrls = set()
    # struct to keep track of metrics
    scrapeMetrics = Metrics()
    testSimple = Simple_List()

    # find time at which to stop analyzing
    stopTime = round(time() + runTime)

    def enqueue_urlList(urlList):
        """
        Cleans and enqueues URLs contained in urlList, checking if
        previously scraped
        """
        for url in urlList:
            if not url in scrapedUrls:
                scrapedUrls.add(url)
                urlQueue.put(url)

    def worker():
        """ Scrapes popped URL from urlQueue and stores data in database"""
        while True:
            # pop top url from queue
            url = urlQueue.get()

            try:
                pageDict = scrape_url(url, knowledgeProcessor, freqDict)
                # pull list of links from pageDict and put in urlQueue
                # enqueue_urlList(pageDict['linkList'])
                testSimple.add(pageDict)
                # update scrape metrics
                scrapeMetrics.add(error=False)

            except Exception as e:
                scrapeMetrics.add(error=True)

            # save progress every 10 items
            if (len(testSimple.data) == 10):
                # testSimple.save(f"data/thicctable/{str(scrapeMetrics.count)}")
                save(testSimple.data, f'data/thicctable/{str(scrapeMetrics.count + 345)}')
                testSimple.clear()
                pass

            # log progress
            print(f"\tURLs ANALYZED: {scrapeMetrics.count} | Errors: {scrapeMetrics.errors} | Queue Size: {urlQueue.qsize()}", end="\r")
            # signal completion
            urlQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # load cleaned initial urls into url_queue
    urlList = list(map(lambda url:fix_url(url, url), urlList))
    enqueue_urlList(urlList)

    # ensure all urlQueue processes are complete before proceeding
    urlQueue.join()

    return True
