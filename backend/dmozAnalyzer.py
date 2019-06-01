import pandas as pd
import crawlers.crawler as crawler
import time
import crawlers.urlAnalyzer as ua
import crawlers.htmlAnalyzer as ha

dmozDF = pd.read_csv("data/test.tab.tsv", sep="\t", names=["url", "path"])

def scrape_dmoz_line(line):
    """ Converts line of dmoz dataframe to tuple of pageText and top folder """

def scrape_dmoz(df):
    """ Scrapes dmoz dataframe of urls and folders to return dataframe of
    readable pageText"""

    for index, row in df.iterrows():
        row['url'] = 0

scrape_dmoz(dmozDF)

print(dmozDF)
