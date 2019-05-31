# Script responsible for building database of page data from list of URLs.
# Outsources all HTML processing to htmlAnalyzer. Handels url requesting and
# Thread/Queue model for distributed parsing

import urllib.request
import htmlAnalyzer as ha
import matplotlib.pyplot as plt


class ParseError(Exception):
    """ Exception for errors while parsing a link """
    pass


def clean_url(url):
    """ Add proper headings URLs for crawler analysis """
    # cast url to string
    urlString = str(url)
    if not ha.parsable(urlString)
        # check starts
        if urlString.startswith('http'):
            pass
        elif urlString.startswith("www"):
            urlString = "http://" + urlString
        else:
            urlString = "http://www." + urlString
    return urlString


def url_to_string(url):
    """ Cleans and converts string of URL link to string of page contents """
    # add proper headers to url
    cleanedURL = clean_url(url)
    try:
        # get http.client.HTTPResponse object of url
        page = urllib.request.urlopen(cleanedURL)
    except:
        raise ParseError(f"Unable to access '{cleanedURL}''")
    pageString = page.read()
    page.close()
    return(pageString)


def urlList_to_stringList(urlList):
    errors = 0
    stringList = []
    for count, url in enumerate(urlList):
        try:
            urlString = url_to_string(url)
            stringList.append(url_to_string(url))
        except:
            stringList.append("ERROR")
            errors += 1
        print(f"\t{count} urls analyzed with {errors} errors", end="\r")
    return stringList

### CRAWLING STUFF ##
from queue import Queue
from threading import Thread

def worker():
    """ Worker to process popped URL from URL Queue """
    # set globals
    global test_parseList
    global test_errors
    # pop url from queue and analyze
    while True:
        url = url_queue.get()
        try:
            # convert url to string of html contents
            pageString = ua.url_to_string(url)
            # grab data from html
            pageDict = ha.analyze_html(pageString)
            print(pageDict)
        except:
            print(f"ERROR: {url}")

def scrape_urlList(urlList, queueDepth, workerNum):
    """
    Args: urlList to scrape, depth of url_queue, number of workers to spawn
    Returns: wide column store of data from each url
    """
    # initialize globals
    test_parseList = []
    test_errors = []
    # initialize url_queue
    url_queue = Queue(10)
    # spawn workerNum workers
    for _ in range(20):
        t = Thread(target=worker)
        t.daemon = True
        t.start()




def scrape_urlList_deep(urlList, maxNum, disp=False):
    """ Iterate through list of URLs, adding title, url, and links to webDF """
    count, errors = 0, 0
    pageDictList = []
    searchedURLs = set()
    # lists to store disp metrics
    lenList, errorList = [], []
    # continue iterating until no more links can be found
    while (urlList != []) and (count <= maxNum):
        # curURL to analyze is the head of urlList
        curURL = urlList[0]
        if curURL not in searchedURLs:
            searchedURLs.add(curURL)
            try:
                # scrape text from link
                curPageString = url_to_string(curURL)
                # get title from pageString
                curTitle = htmlAnalyzer.find_title(curPageString)
                # get links from page string
                curLinks = htmlAnalyzer.find_links(curPageString)
                # get meta tag descriptions
                curDescriptions = htmlAnalyzer.find_descriptions(curPageString)
                # get time of loading
                loadTime = datetime.datetime.now()
                # create dict of page info
                curPageDict = {'title':curTitle, 'url':curURL, 'links':curLinks, 'descriptions':curDescriptions,  'loadTime':loadTime}
                pageDictList.append(curPageDict)
                # add curLinks to urlList for analysis
                urlList += curLinks
            except:
                errors += 1
            # remove first item in urlList
            del urlList[0]
            # increment count, lenList, and errorList
            count += 1
            lenList.append(len(urlList))
            errorList.append(errors)
        else:
            # if a url thats already been hit is found, finish scraping
            urlList = []

        # print progress
        print(f"\t{count} URLs analyzed with {errors} errors!\r", end="")

        if ((count % 20) == 0):
            # display metrics if asked
            if disp:
                plt.plot(lenList)
                plt.plot(errorList)
                plt.legend(['Number URLs to Analyze', 'Number Error URLs'])
                plt.title("Scrape Metrics")
                plt.xlabel("Iterations")
                plt.ylabel("Number URLs")
                plt.savefig("scrapeMetrics")

    # create dataframe of scraped info
    scrapedDF = pd.DataFrame(pageDictList)
    return(scrapedDF)

#
# sampleStr = url_to_string("https://stackoverflow.com")
#
# test = htmlAnalyzer.find_links(sampleStr)
#
# testDF = scrape_urlList(test, 50, True)
#
# # testDF.to_csv('testDF.csv', sep=',')
