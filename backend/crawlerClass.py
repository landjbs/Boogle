import urllib

def scrape_url(url):
    page = urllib.urlopen(url)
    outstr = "".join([line for line in page])
    page.close()
