# Responsible for gathering and processing data from HTML pageStrings.
# pageStrings generally passed from crawler.py after being cleaned by
# urlAnalyzer.py. Outsources all NLP and ML to backend/models.

import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup
import crawlers.urlAnalyzer as ua



# image string
imageString = '(?<=src=")' + "\S+" + '(?=")'
imageMatcher = re.compile(imageString)


# matcher for url denoted by https:// or http://
urlString = r'https://\S+|http://\S+'
urlMatcher = re.compile(urlString)


def clean_pageText(rawText):
    """ Removes junk from output of soup.get_text() """
    cleanText = rawText.replace("\n","")
    # cleanText = cleanText.replace("\t","")
    return cleanText


def get_pageText(pageString):
    """
    Gets only pageText from pageString using BeautifulSoup.
    Requires recreation of BeautifulSoup() object so don't call in
    htmlAnalyzer.py.
    """
    curSoup = BeautifulSoup(pageString, "html.parser")
    rawText = curSoup.get_text()
    cleanText = clean_pageText(rawText)
    return cleanText


def parsable(url):
    """ Returns true if url follows urlMatcher pattern """
    # canParse = False if not urlMatcher.match(url) else False
    canParse = True if urlMatcher.fullmatch(url) else False
    return canParse


def get_links(soup):
    """ Returns list of all valid links from pageString """
    # get list of all <a> tags in soup
    a_list = soup.find_all('a', href=True)
    # get list of validated urls from <a> tag list
    linkList = [link['href'] for link in a_list if parsable(link['href'])]
    return linkList


def detect_language(pageString):
    """ Detects language of a pageString """
    lang, score = langid.classify(pageString)
    return(lang)


def analyze_html(pageString):
    """
    Args: pageString to analyze (usually passed from urlAnalyzer)
    Returns: TO DO
    """
    # create a soup object for parsing pageString
    curSoup = BeautifulSoup(pageString, "html.parser")
    ## strip data from curSoup
    # get string in <title></title> tags
    title = curSoup.title.string
    # get all readable text on the page
    raw_pageText = curSoup.get_text()
    # get list of valid links
    linkList = get_links(curSoup)
    # MORE HERE—loadTime should be last!
    # time at which the url data was loaded into memory
    loadTime = ()
    # set outs
    outDict = {'title':title, 'linkList':linkList, 'loadTime':loadTime}
    return outDict

def scrape_url(url):
    """
    Fetches and processes url and returns tuple of page info with None score
    """
