import urllib.request
import htmlAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

class ParseError(Exception):
    """ Exception for errors while parsing a link """
    pass

def scrape_url(url):
    """ Converts string of URL link to string of page contents """
    try:
        # get http.client.HTTPResponse object of url
        page = urllib.request.urlopen(url)
    except:
        raise ParseError(f"Unable to access '{url}''")

    def decode_line(line):
        """ Helper to decode and consolidate line of html """
        try:
            decodedLine = line.decode("utf-8")
            return decodedLine
        # returns empty string if unable to decode
        except:
            return("")

    # convert decoded lines of page to string
    outstr = "".join([decode_line(line) for line in page])
    page.close()
    return(outstr)


def scrape_urlList(urlList, maxNum, disp=False):
    """ Iterate through list of URLs, adding title, url, and links to webDF """
    count, errors = 0, 0
    pageDictList = []
    # init disp store
    lenList = []
    # continue iterating until no more links can be found
    while (urlList != []) and (count <= maxNum):
        # curURL to analyze is the head of urlList
        curURL = urlList[0]
        try:
            # scrape text from link
            curPageString = scrape_url(curURL)
            # get title from pageString
            curTitle = htmlAnalyzer.find_title(curPageString)
            # get links from page string
            curLinks = htmlAnalyzer.find_links(curPageString)
            # create dict of page info
            curPageDict = {'Title':curTitle, 'URL':curURL, 'Links':curLinks, 'Contents':curPageString}
            pageDictList.append(curPageDict)
            # add curLinks to urlList for analysis
            urlList += curLinks
        except:
            errors += 1
        # remove first item in urlList
        del urlList[0]
        # increment count and urList_len
        count += 1
        lenList.append(len(urlList))
        # print progress
        print(f"\t{count} URLs analyzed with {errors} errors!\r", end="")
    # display metrics if asked
    if disp:
        plt.plot(lenList)
        plt.title("Length of URL List Over Time")
        plt.xlabel("Iterations")
        plt.ylabel("Length of URL List")
        plt.show()
    # create dataframe of scraped info
    scrapedDF = pd.DataFrame(pageDictList, columns=["Title", "URL", "Links", "Contents"])
    return(scrapedDF)

sampleStr = scrape_url("https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping")

test = htmlAnalyzer.find_links(sampleStr)

testDF = scrape_urlList(test, 100, True)
