# Responsible for building database of page data from list of URLs.
# Outsources URL processing to urlAnalyzer.py
# Outsources HTML processing to htmlAnalyzer.py
# Outsoucres database definitions to thicctable.py

from queue import Queue
from threading import Thread
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha
from dataStructures.simpleStructures import Simple, Metrics

def scrape_urlList(urlList, queueDepth=10, workerNum=20, maxLen=100, outPath=""):
    """
    Builds wide column store of url data from urlList with recursive search
    Args: urlList to scrape, depth of url_queue, number of workers to spawn
    Returns: wide column store of data from each url
    """
    # queue to hold urlList
    urlQueue = Queue(queueDepth)
    # struct to hold scraped data
    outStore = Simple()
    # struct to keep track of metrics
    scrapeMetrics = Metrics()

    def worker():
        """ Scrapes popped URL from urlQueue and stores data in outStore()"""
        while True:
            # pop top url from queue
            url = urlQueue.get()
            try:
                # convert url to string of html contents
                pageString = ua.url_to_pageString(url, timeout=5)
                # grab data from html
                pageDict = ha.analyze_html(pageString)
                # add pageDict to outStore
                outStore.add(pageDict)
                # update scrape metrics
                scrapeMetrics.add(error=False)
                print(f"SUCCESS: {url}")
            except:
                # update scrape metrics
                scrapeMetrics.add(error=True)
                print(f"\tERROR: {url}")
            # log progress
            print(f"\t{scrapeMetrics.count} URLs analyzed with {scrapeMetrics.errors} errors!", end="\r")
            # signal completion
            urlQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # load cleaned urls into url_queue
    for url in urlList:
        cleanedURL = ua.clean_url(url)
        urlQueue.put(url)

    # ensure all urlQueue processes are complete before proceeding
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
