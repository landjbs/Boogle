import pandas as pd
import crawlers.crawler as crawler
import re
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha

# matcher for url in dmozDF line
urlString = r'(?<=").+(?="\t)'
urlMatcher = re.compile(urlString)

# matcher for top folder in dmozDF line
folderString = r'(?<="Top/).+(?=/)'
folderMatcher = re.compile(folderString)

# import dmoz data
dmozDF = pd.read_csv("data/test.tab.tsv", sep="\t", names=["url", "path"])

def scrape_dmoz_line(line):
    """ Converts line of dmoz dataframe to tuple of pageText and top folder """
    # find url and top folder with re
    url = urlMatcher.findall(line)
    folder = folderMatcher.findall(line)
    # fetch pageString from url
    pageString = ua.url_to_pageString(url)
    # get rendered text on pageString
    pageText = ha.get_pageText(pageString)
    # get top folder


def scrape_dmoz(df):
    """ Scrapes dmoz dataframe of urls and folders to return dataframe of
    readable pageText"""

    for index, row in df.iterrows():
        row['url'] = 0

scrape_dmoz(dmozDF)

print(dmozDF)
