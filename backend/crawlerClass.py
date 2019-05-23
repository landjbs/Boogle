import urllib.request
import htmlAnalyzer
import pandas as pd

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
            decodedLine = (line).decode("utf-8")
            return decodedLine
        # returns empty string if unable to decode
        except:
            return("")

    # convert decoded lines of page to string
    outstr = "".join([decode_line(line) for line in page])
    page.close()
    return(outstr)

webDF = pd.DataFrame(index=["Title", "URL", "Links"])
print(webDF)

def scrape_urlList(urlList):
    """ Iterate through list of URLs, adding title, url, and links to webDF """
    errors = 0
    for count, link in enumerate(urlList):
        print(f"\t{count} URLs analyzed with {errors} errors!\r", end="")
        try:
            # scrape text from link
            curPageString = scrape_url(link)
            # get title from pageString
            curTitle = htmlAnalyzer.find_title(curPageString)
            # get links from page string
            urlLinks = htmlAnalyzer.find_links(curPageString)
        except:
            errors += 1
    print(urlHolder)


sampleStr = scrape_url("https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping")

test = htmlAnalyzer.find_links(sampleStr)

scrape_urlList(test)
