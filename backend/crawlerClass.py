import urllib.request
import htmlAnalyzer
import pandas as pd
import datetime
import matplotlib.pyplot as plt

class ParseError(Exception):
    """ Exception for errors while parsing a link """
    pass


def decode_line(line):
    """ Helper to decode and consolidate line of html """
    try:
        decodedLine = line.decode("utf-8")
    # return empty string if unable to decode byte
    except:
        decodedLine = ""
    return decodedLine


def url_to_string(url):
    """ Converts string of URL link to string of page contents """
    try:
        # get http.client.HTTPResponse object of url
        page = urllib.request.urlopen(url)
    except:
        raise ParseError(f"Unable to access '{url}''")
    # convert decoded lines of page to string
    outstr = "".join([decode_line(line) for line in page])
    page.close()
    return(outstr)


def scrape_urlList(urlList, maxNum, disp=False):
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
        if curULS not in searchedURLs:
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
            pass

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

    print(f"Accurate: {searchedURLs == }")
    # create dataframe of scraped info
    scrapedDF = pd.DataFrame(pageDictList)
    return(scrapedDF)


def homepage(scrapedDF):
    """ Searches DF for page """
    rawSearch = input("Search: ")
    tokenSearch = rawSearch.split(" ")
    result = scrapedDF[scrapedDF['title'].str.contains(rawSearch)]
    print(result)


sampleStr = scrape_url("https://stackoverflow.com")

test = htmlAnalyzer.find_links(sampleStr)

testDF = scrape_urlList(test, 50, True)

testDF.to_csv('testDF.csv', sep=',')
