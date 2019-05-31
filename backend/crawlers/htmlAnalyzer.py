# Script responsible for returning processed data from HTML pageString
# passed from urlAnalyzer. Outsources all NLP and ML to backend/models.

import re
import datetime # to find the loadTime of a page
from bs4 import BeautifulSoup

# image string
imageString = '(?<=src=")' + "\S+" + '(?=")'
imageMatcher = re.compile(imageString)

# matcher for url denoted by https:// or http://
urlString = r'https://\S+|http://\S+'
urlMatcher = re.compile(urlString)

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
    pageText = soup.get_text()
