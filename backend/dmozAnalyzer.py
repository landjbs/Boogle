import pandas as pd
from crawlers.urlAnalyzer import url_to_pageString
from crawlers.htmlAnalyzer import get_pageText, detect_language
import re
from threading import Thread
from queue import Queue
from dataStructures.simpleStructures import Simple, Metrics
import models.categorizer.textVectorizer as tv


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
    # find url, top, and folder with regexp match
    url = (urlMatcher.findall(line))[0]
    folder = (folderMatcher.findall(line))[0]
    top = (topMatcher.findall(line))[0]
    # fetch pageString from url
    pageString = url_to_pageString(url)
    # get rendered text on pageString
    pageText = get_pageText(pageString)
    # skip page if not in english
    assert (detect_language(pageText) == 'en'), f"{url} not in English"
    # create list of training data to append to Simple struct
    outList = [url, top, folder, pageText]
    return outList


def scrape_dmoz_file(file, queueDepth=15, workerNum=25, outPath=""):
    """
    Scrapes dmoz tsv file of urls and folders to return dataframe of
    url, folder path, top folder, and readable pageText. Saves dataframe as
    tsv in outPath if specifed.
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
    # convert dict list to dataframe for easy visualization and training
    print(f"\nAnalysis complete! Data scraped from {len(outStore.data)} URLs.")
    # save dataframe to csv in outPath if specifed
    if not (outPath == ""):
        outStore.to_csv(outPath, sep="X_A_B_Z_OTOKENTNE_SADFSFASD")
    return(outStore)


def read_dmoz_csv(file, sep):
    """ Wrapper for pd.read_csv to fit specifics of dmoz data """
    df = pd.read_csv("data/outData/scrapedDMOZ.tab.tsv",
                        sep=sep,
                        skip_blank_lines=True,
                        names=["url", "top", "path", "pageText"],
                        usecols=[0, 1, 2, 3],
                        engine="python")
    return df


# scrape_dmoz_file(file="data/inData/dmoz_domain_category.tab.tsv", queueDepth=15, workerNum=25,
#     outPath="data/outData/scrapeDMOZ.tab.csv")

dmozSimple = scrape_dmoz_file(file="data/inData/test.tab.tsv")

dmozDF = pd.DataFrame(dmozSimple.data, columns=["url", "top", "path", "pageText"])

print("DMOZ HEAD:\n\n:", dmozDF.head, end=f"{'-'*40}")

dmozDF['pageText'] = dmozDF['pageText'].appy(lambda text : tv.tokenize(text))

print(f"\n\n{'-'*60}\nDMOZ MODIFIED: {dmozDF.head}\n{'-'*60}")





pass
