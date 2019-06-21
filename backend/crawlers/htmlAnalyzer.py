"""
Responsible for gathering and processing data from HTML pageStrings.
pageStrings generally passed from crawler.py after being cleaned by
urlAnalyzer.py. Outsources all NLP and ML to backend/models.
Bulkiest function is scrape_url which takes in a url and returns a
page object of page info.
"""

# import sys, os
# sys.path.append(os.path.abspath(os.path.join('..')))
import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup
import crawlers.urlAnalyzer as urlAnalyzer
from models.processing.cleaner import clean_text, clean_title, clean_url
from models.knowledge.knowledgeFinder import score_divDict
from dataStructures.pageObj import Page

# image matcher
imageMatcher = re.compile('(?<=src=")\S+(?=")')

# matcher for all h-number tages in html text
headerMatcher = re.compile('^h[1-6$]')


def clean_pageText(rawText, title):
    """ Removes junk from output of soup.get_text() """
    # find location of end of the title in rawText
    titleEnd = rawText.find(title) + len(title)
    # filter out everything before the title
    afterTitle = rawText[titleEnd:]
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


def scrape_url(url, knowledgeProcessor, freqDict, timeout=4):
    """
    Fetches and processes url and returns list of page info.
    Data Returned:
        -url: url of the page (cleaned by urlAnalyzer.fix_url)
        -title: cleanedd title of the page
        -knowledgeTokens: dict of knowledge tokens and their scores
        -linkList: list of urls found on the page
        -loadTime: Time in seconds the page took to load (rounded to 10ths)
        -loadDate: Time at which the page was loaded in days since 1970
    """

    # fetch page string and save time to load
    loadStart = time.time()
    rawString = urlAnalyzer.url_to_pageString(url, timeout=timeout)
    loadEnd = time.time()

    # round time page took to load to 10ths
    loadTime = round(loadEnd - loadStart, ndigits=1)
    # number of days since 1970 when page was loaded
    loadDate = int(loadEnd / (86400))

    # create soup object for parsing pageString
    curSoup = BeautifulSoup(rawString, 'html.parser')
    # pull title and text from soup object
    title = (curSoup.title.string)
    cleanedText = clean_pageText(curSoup.get_text(), title)

    # validate language
    assert (detect_language(cleanedText)=='en'), f"{url} contents not in English"

    # find list of headers in soup object
    headerList = curSoup.find_all(headerMatcher)
    # join cleaned headers into space delimited string
    headers = " ".join(clean_text(str(header)) for header in headerList)

    # find contents of discription tag in soup object if it exists
    try:
        description = curSoup.find('meta', attrs={'name': 'description'}).get('content')
    except:
        description = ""

    # find contents of keyword tag in soup object if it exists
    try:
        keywords = curSoup.find('meta', attrs={'name':'keywords'}).get('content')
    except:
        keywords = ""

    # create dict of divs and contents for knowledge tokenization
    divDict = {'url':url,'title':title, 'headers':headers, 'description':clean_text(description), 'keywords':clean_text(keywords),'all':cleanedText}

    # find dict mapping knowledge tokens in divDict to their score
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)

    # find and clean list of links from soup object
    linkList = list(map(lambda url : urlAnalyzer.fix_url(url), get_links(curSoup)))

    # decide text to use for window display; description if possible
    windowText = description if (description != "") else cleanedText

    # DOC VEC BELOW

    # return list of information about page
    return Page(clean_url(url), clean_title(title), knowledgeTokens, linkList, loadTime, loadDate, windowText)











pass
