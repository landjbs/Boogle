import urllib.request
import htmlAnalyzer

class ParseError(Exception):
    pass

def scrape_url(url):
    """ Converts string of url link to string of page contents """
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

def scrape_urlList(urlList):
    errors = 0
    for c, link in enumerate(urlList):
        print(f"\t{c}\r", end="")
        try:
            scrape_url(link)
        except:
            errors += 1
    print(f"{len(urlList)} urls analyzed with {errors} errors!")

sampleStr = scrape_url("https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping")

test = htmlAnalyzer.find_links(sampleStr)

scrape_urlList(test)
