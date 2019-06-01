import pandas as pd
import crawlers.crawler as crawler
import re
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha


# matcher for url in dmozDF line
urlString = r'(?<=").+(?="\t)'
urlMatcher = re.compile(urlString)


# matcher for top folder in dmozDF line
folderString = r'(?<="Top/)[a-z|A-Z]+(?=/)'
folderMatcher = re.compile(folderString)


def scrape_dmoz_line(line):
    """ Converts line dmoz tsv file to tuple of pageText and top folder """
    # find url and top folder with re
    url = urlMatcher.findall(line)
    folder = folderMatcher.findall(line)
    # fetch pageString from url
    pageString = ua.url_to_pageString(url)
    # get rendered text on pageString
    pageText = ha.get_pageText(pageString)
    return (folder)


def scrape_dmoz():
    """ Scrapes dmoz tsv file of urls and folders to return dataframe of
    readable pageText"""

    with open("data/test.tab.tsv", 'r') as FileObj:
        for line in FileObj:
            line = str(line)
            try:
                print(scrape_dmoz_line(line))
            except:
                print("\r", end="\r")



scrape_dmoz()
