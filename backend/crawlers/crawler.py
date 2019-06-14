# Responsible for building database of page data from list of URLs.
# Outsources URL processing to urlAnalyzer.py
# Outsources HTML processing to htmlAnalyzer.py
# Outsoucres database definitions to thicctable.py

import os
from queue import Queue
from threading import Thread
import crawlers.urlAnalyzer as urlAnalyzer
import crawlers.htmlAnalyzer as htmlAnalyzer
import models.knowledge.knowledgeBuilder as knowledgeBuilder
from dataStructures.simpleStructures import Metrics
from dataStructures.thicctable import Thicctable
from dataStructures.objectSaver import save, load

import time

def scrape_urlList(urlList, knowledgeProcessor, queueDepth=10, workerNum=20, maxLen=100, outPath=""):
    """
    Builds wide column store of url data from urlList with recursive search
    Args: urlList to scrape, depth of url_queue, number of workers to spawn
    Returns: wide column store of data from each url
    """
    # # load knowledge set and use to initialize databasse
    knowledgeSet = load('data/outData/knowledge/knowledgeSet.sav')
    database = Thicctable(knowledgeSet)
    del knowledgeSet

    # load knowledge data
    freqDict = load('data/outData/knowledge/freqDict.sav')

    # queue to hold urlList
    urlQueue = Queue(queueDepth)
    # set to hold , previously scraped URLs
    scrapedUrls = set()
    # struct to keep track of metrics
    scrapeMetrics = Metrics()

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
                pageList = htmlAnalyzer.scrape_url(url, knowledgeProcessor, freqDict)
                database.bucket_page(pageList)
                # pull list of links from pageDict and put in urlQueue
                # enqueue_urlList(pageList[3])
                # update scrape metrics
                scrapeMetrics.add(error=False)
            except Exception as e:
                print(e)
                # update scrape metrics
                scrapeMetrics.add(error=True)
            # log progress
            print(f"\t{scrapeMetrics.count} URLs analyzed with {scrapeMetrics.errors} errors!", end="\r")
            # signal completion
            urlQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # load cleaned initial urls into url_queue
    urlList = list(map(lambda url:urlAnalyzer.clean_url(url), urlList))
    enqueue_urlList(urlList)

    # ensure all urlQueue processes are complete before proceeding
    urlQueue.join()


    return database
