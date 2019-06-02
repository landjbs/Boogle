import pandas as pd
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha
import re
from threading import Thread
from queue import Queue
from dataStructures.simpleStructures import Simple, Metrics


### Match objects compiled for quick calls in functions ###
# matcher for url in dmozDF line
urlString = r'(?<=").+(?="\t)'
urlMatcher = re.compile(urlString)

# matcher for folder in dmozDF line
folderString = r'(?<=Top/)\S+(?=")'
folderMatcher = re.compile(folderString)

# matcher for top folder in dmozDF line
topString = r'(?<="Top/)[^/]+'
topMatcher = re.compile(topString)


### Functions to scrape dmoz tsv file into dataframe for model training ###
def scrape_dmoz_line(line):
    """ Helper to convert line dmoz tsv file to dict of url, folder path,  """
    # find url, top, and folder with re
    url = (urlMatcher.findall(line))[0]
    folder = (folderMatcher.findall(line))[0]
    top = (topMatcher.findall(line))[0]
    # fetch pageString from url
    pageString = ua.url_to_pageString(url)
    # get rendered text on pageString
    pageText = ha.get_pageText(pageString)
    # skip page if not in english
    assert (ha.detect_language(pageText) == 'en'), f"{url} not in English"
    # create dict of training data to append to list (index because re returns list)
    outDict = {'url':url, 'folder':folder, 'top':top, 'pageText':pageText}
    return outDict


def scrape_dmoz_file(file, queueDepth=10, workerNum=20):
    """
    Scrapes dmoz tsv file of urls and folders to return dataframe of
    url, folder path, top folder, and readable pageText
    """
    # queue to hold lines of file
    lineQueue = Queue(queueDepth)
    # struct (list) to hold scraped data
    outStore = Simple()
    # struct to keep track of metrics
    scrapeMetrics = Metrics()

    def worker():
        """ Analyzes popped line from lineQueue and stores data in outStore() """
        while True:
            line = lineQueue.get()
            try:
                # call helper to scrape line
                pageDict = scrape_dmoz_line(line)
                # add scraped pageDict to outStore list
                outStore.add(pageDict)
                # update scrape metrics
                scrapeMetrics.add(error=False)
            except:
                # update scrape metrics
                scrapeMetrics.add(error=True)
            # log progress
            print(f"\t{scrapeMetrics.count} URLs analyzed with {scrapeMetrics.errors} errors!", end="\r")
            # signal completion
            lineQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # load lines from file into lineQueue
    with open(file, 'r') as FileObj:
        for line in (FileObj):
            lineQueue.put(line)
    # ensure all lineQueue processes are complete before proceeding
    lineQueue.join()

    outDF = pd.DataFrame(outStore.data)

    return(outDF)




print(scrape_dmoz_file("inData/test.tab.tsv").head)
