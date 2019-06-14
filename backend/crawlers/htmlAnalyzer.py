# Responsible for gathering and processing data from HTML pageStrings.
# pageStrings generally passed from crawler.py after being cleaned by
# urlAnalyzer.py. Outsources all NLP and ML to backend/models.

# import sys, os
# sys.path.append(os.path.abspath(os.path.join('..')))
import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup
import crawlers.urlAnalyzer as urlAnalyzer
from models.processing.cleaner import clean_text
from models.knowledge.knowledgeFinder import score_divDict
# from models.knowledge.knowledgeReader import find_knowledgeTokens


# image matcher
imageMatcher = re.compile('(?<=src=")\S+(?=")')

# matcher for all h-number tages in html text
headerMatcher = re.compile('^h[1-6$]')

def clean_pageText(rawText, title):
    """ Removes junk from output of soup.get_text() """
    # find location of title in rawText
    titleLoc = rawText.find(title)
    # filter out everything before the title
    afterTitle = rawText[titleLoc:]
    # call clean_text from models.textProcessor.cleaner
    cleanedText = clean_text(afterTitle)
    return cleanedText


def get_pageText(url):
    """
    Gets only pageText from url using BeautifulSoup and urlAnalyzer.
    Requires recreation of BeautifulSoup() object so don't call in
    htmlAnalyzer.py.
    """
    rawString = urlAnalyzer.url_to_pageString(url)
    curSoup = BeautifulSoup(rawString, "html.parser")
    rawText = curSoup.get_text()
    title = curSoup.title.string
    cleanedText = clean_pageText(rawText, title)
    return cleanedText


def get_links(soup):
    """
    Returns list of all valid links from pageString.
    Must work on raw string: cleaning destroys links!
    """
    # get list of all <a> tags in soup
    a_list = soup.find_all('a', href=True)
    # get list of validated urls from <a> tag list
    linkList = [link['href'] for link in a_list if urlAnalyzer.parsable(link['href'])]
    return linkList


def detect_language(pageString):
    """ Detects language of a pageString """
    lang, score = langid.classify(pageString)
    return lang


def scrape_url(url, knowledgeProcessor, freqDict):
    """
    Fetches and processes url and returns list of page info.
    Data Returned:
        -url: unedited url of the page
        -title: title of the page
        -
        -loadTime: Time in seconds the page took to load (rounded to 10ths)
        -loadDate: Time at which the page was loaded in days since 1970
        -
    """
    # fetch page string and save time to load
    loadStart = time.time()
    rawString = urlAnalyzer.url_to_pageString(url, timeout=4)
    loadEnd = time.time()

    # round time page took to load to 10ths
    loadTime = round(loadEnd - loadStart, ndigits=1)
    # number of days since 1970 when page was loaded
    loadDate = int(loadEnd / (86400))

    # create soup object for parsing pageString
    curSoup = BeautifulSoup(rawString, 'html.parser')
    # pull title and text from soup object
    title = curSoup.title.string
    cleanedText = clean_pageText(curSoup.get_text(), title)

    # validate language
    assert (detect_language(cleanedText)=='en'), f"{url} not in English"

    # find list of headers in soup object
    headerList = curSoup.findAll(headerMatcher)
    # join cleaned headers into space delimited string
    headers = " ".join(clean_text(str(header)) for header in headerList)

    # create dict of divs and contents for knowledge tokenization
    divDict = {'title':title, 'headers':headers, 'all':cleanedText}

    # find dict mapping knowledge tokens in divDict to their score
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)

    # find and clean list of links from soup object
    linkList = list(map(lambda link:urlAnalyzer.clean_url(url), get_links(curSoup)))

    # find roungh number of words in page
    pageLength = len(cleanedText.split(" "))

    # return list of information about page
    return [url, title, knowledgeTokens, linkList, pageLength, loadTime, loadDate]











pass
