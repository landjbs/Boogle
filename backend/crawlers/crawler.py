# Script responsible for building database of page data from list of URLs.
# Outsources URL processing to urlAnalyzer.
# Outsources HTML processing to htmlAnalyzer.
# Outsoucres database definitions to thicctable.py

from queue import Queue
from threading import Thread

class Store():
    """ Test class composed of list to which pageDicts are added """
    def __init__(self):
        self.data = []
    def add(self, elt):
        self.data += [(elt)]

class Metrics():
    """ Class to keep track of scrape progress """
    def __init__(self):
        self.count = 0
        self.errors = 0

    def add(self, error=False):
        self.count += 1
        if error:
            self.errors += 1

def scrape_urlList(urlList, queueDepth=10, workerNum=20):
    """
    Builds wide column store of url data from urlList with no recursive search
    Args: urlList to scrape, depth of url_queue, number of workers to spawn
    Returns: wide column store of data from each url
    """
    # queue to hold urlList
    urlQueue = Queue(queueDepth)
    # struct to hold scraped data
    outStore = Store()
    # struct to keep track of metrics
    scrapeMetrics = Metrics()

    def worker():
        """ Worker to process popped URL from URL Queue """
        # pop url from queue and analyze
        while True:
            url = urlQueue.get()
            try:
                # convert url to string of html contents
                pageString = url_to_pageString(url)
                # grab data from html
                pageDict = ha.analyze_html(pageString)
                # print(f"{url}: {pageDict}")
                # print(f"SUCCESS: {url}")
                outStore.add(pageDict)
                scrapeMetrics.add()
            except:
                scrapeMetrics.add(error=True)
            print(f"\t{scrapeMetrics.count} URLs analyzed with {scrapeMetrics.errors} errors!", end="\r")
            urlQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()
    # load cleaned urls into url_queue
    for url in urlList:
        cleanedURL = clean_url(url)
        urlQueue.put(url)
    # ensure all url_queue processes are complete before proceeding
    urlQueue.join()
    return outStore









# def scrape_urlList_deep(urlList, maxNum, disp=False):
#     """ Iterate through list of URLs, adding title, url, and links to webDF """
#     count, errors = 0, 0
#     pageDictList = []
#     searchedURLs = set()
#     # lists to store disp metrics
#     lenList, errorList = [], []
#     # continue iterating until no more links can be found
#     while (urlList != []) and (count <= maxNum):
#         # curURL to analyze is the head of urlList
#         curURL = urlList[0]
#         if curURL not in searchedURLs:
#             searchedURLs.add(curURL)
#             try:
#                 # scrape text from link
#                 curPageString = url_to_string(curURL)
#                 # get title from pageString
#                 curTitle = htmlAnalyzer.find_title(curPageString)
#                 # get links from page string
#                 curLinks = htmlAnalyzer.find_links(curPageString)
#                 # get meta tag descriptions
#                 curDescriptions = htmlAnalyzer.find_descriptions(curPageString)
#                 # create dict of page info
#                 curPageDict = {'title':curTitle, 'url':curURL, 'links':curLinks, 'descriptions':curDescriptions,  'loadTime':loadTime}
#                 pageDictList.append(curPageDict)
#                 # add curLinks to urlList for analysis
#                 urlList += curLinks
#             except:
#                 errors += 1
#             # remove first item in urlList
#             del urlList[0]
#             # increment count, lenList, and errorList
#             count += 1
#             lenList.append(len(urlList))
#             errorList.append(errors)
#         else:
#             # if a url thats already been hit is found, finish scraping
#             urlList = []
#
#         # print progress
#         print(f"\t{count} URLs analyzed with {errors} errors!\r", end="")
#
#         if ((count % 20) == 0):
#             # display metrics if asked
#             if disp:
#                 plt.plot(lenList)
#                 plt.plot(errorList)
#                 plt.legend(['Number URLs to Analyze', 'Number Error URLs'])
#                 plt.title("Scrape Metrics")
#                 plt.xlabel("Iterations")
#                 plt.ylabel("Number URLs")
#                 plt.savefig("scrapeMetrics")
#
#     # create dataframe of scraped info
#     scrapedDF = pd.DataFrame(pageDictList)
#     return(scrapedDF)
#
# #
# # sampleStr = url_to_string("https://stackoverflow.com")
# #
# # test = htmlAnalyzer.find_links(sampleStr)
# #
# # testDF = scrape_urlList(test, 50, True)
# #
# # # testDF.to_csv('testDF.csv', sep=',')
