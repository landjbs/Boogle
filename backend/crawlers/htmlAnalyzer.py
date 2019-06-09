# Responsible for gathering and processing data from HTML pageStrings.
# pageStrings generally passed from crawler.py after being cleaned by
# urlAnalyzer.py. Outsources all NLP and ML to backend/models.

# import sys, os
# sys.path.append(os.path.abspath(os.path.join('..')))
import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup
import crawlers.urlAnalyzer as ua
from models.textProcessor.cleaner import clean_text


# image string
imageString = '(?<=src=")' + "\S+" + '(?=")'
imageMatcher = re.compile(imageString)


def clean_pageText(rawText, title):
    """ Removes junk from output of soup.get_text() """
    # find location of title in rawText
    titleLoc = rawText.find(title)
    # filter out everything before the title
    afterTitle = rawText[titleLoc:]
    # call clean_text from models.textProcessor.cleaner
    cleanedText = clean_text(afterTitle)
    return cleanedText


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


def get_links(soup):
    """ Returns list of all valid links from pageString """
    # get list of all <a> tags in soup
    a_list = soup.find_all('a', href=True)
    # get list of validated urls from <a> tag list
    linkList = [link['href'] for link in a_list if ua.parsable(link['href'])]
    return linkList


def detect_language(pageString):
    """ Detects language of a pageString """
    lang, score = langid.classify(pageString)
    return(lang)


def scrape_url(url):
    """
    Fetches and processes url and returns tuple of page info with None score
    """
    # fetch page string and save time to load
    loadStart = time.time()
    pageString = ua.url_to_pageString(url)
    loadTime = time.time()
    loadedAt = loadEnd - loadStart
    # create soup object for parsing pageString
    curSoup = BeautifulSoup(pageString, 'html.parser')
    # get string in <title></title> tags
    title = curSoup.title.string
    # get raw_pageText for soup matcher
    raw_pageText = curSoup.get_text()
    # find location of title in raw_pageText
    pageText = clean_pageText(raw_pageText, title)

    # return tuple in form:
    #   (score, title, url, linkList, loadTime)
    dataTuple = (None, title, loadTime, loadedAt)
    return dataTuple
