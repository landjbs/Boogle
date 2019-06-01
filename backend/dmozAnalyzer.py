import pandas as pd
import crawlers.crawler as crawler
import re
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha

# matcher for url in dmozDF line
urlString = r'(?<=").+(?="\t)'
urlMatcher = re.compile(urlString)

# matcher for folder in dmozDF line
folderString = r'(?<=Top/)\S+(?=")'
folderMatcher = re.compile(folderString)

# matcher for top folder in dmozDF line
topString = r'(?<="Top/)[a-z|A-Z]+(?=/)'
topMatcher = re.compile(folderString)


def scrape_dmoz_line(line):
    """ Converts line dmoz tsv file to tuple of pageText and top folder """
    # find url, top, and folder with re
    url = urlMatcher.findall(line)
    folder = folderMatcher.findall(line)
    top = topMatcher.findall(line)
    # fetch pageString from url
    pageString = ua.url_to_pageString(url[0])
    # get rendered text on pageString
    pageText = ha.get_pageText(pageString)
    # skip page if not in english
    if not (ha.detect_language(pageText) == 'en'):
        raise ua.ParseError("Page is not in English")
    # create dict of training data to append to list
    outDict = {'url':url, 'folder':folder, 'top':top, 'pageText':pageText}
    return outDict


def scrape_dmoz_file(file):
    """ Scrapes dmoz tsv file of urls and folders to return dataframe of
    url, folder path, top folder, and readable pageText """

    with open(file, 'r') as FileObj:
        for i, line in enumerate(FileObj):
            if i > 3:
                line = str(line)
                try:
                    print(scrape_dmoz_line(line))
                # print()
                except:
                    print(f"\t{i}", end="\r")



scrape_dmoz_file("data/test.tab.tsv")
