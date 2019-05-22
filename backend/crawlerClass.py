import urllib.request

def scrape_url(url):
    """ Converts string of url link to string of page contents """
    try:
        page = urllib.request.urlopen(url)
    except:
        raise ValueError(f"Unable to access contents of '{url}''")

    def decode_line(line):
        """ Decodes and consolidates line of html """
        decodedLine = (line).decode("utf-8")
        return decodedLine

    outstr = "".join([decode_line(line) for line in page])
    page.close()
    print(outstr)


scrape_url("https://stackoverflow.com/questions/16627227/http-error-403-in-python-3-web-scraping")
