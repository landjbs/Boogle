"""
Responsible for gathering and processing data from HTML pageStrings.
pageStrings generally passed from crawler.py after being cleaned by
urlAnalyzer.py. Outsources all NLP and ML to backend/models.
Bulkiest function is scrape_url which takes in a url and returns a
page object of page info.
"""

import pandas as pd
import numpy as np
import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup # to parse html
from bert_serving.client import BertClient # to assign document vectors
from keras.models import load_model # to classify document vectors

from crawlers.urlAnalyzer import fix_url, url_to_pageString, parsable
from models.processing.cleaner import clean_text, clean_title, clean_url
from models.knowledge.knowledgeFinder import score_divDict
import models.binning.docVecs as dv



# matcher for all h-number tages in html text
h1Matcher = re.compile('^h1$')
h2Matcher = re.compile('^h2$')
h3Matcher = re.compile('^h3$')
lowHeaderMatcher = re.compile('^h[4-6$]')


def clean_pageText(rawText, title):
    """
    Removes junk from output of soup.get_text()
    Returns: completely cleaned text and raw text with title removed
    """
    # find location of end of the title in rawText
    titleEnd = rawText.find(title) + len(title)
    # filter out everything before the title
    afterTitle = rawText[titleEnd:]
    # call clean_text from models.textProcessor.cleaner
    cleanedText = clean_text(afterTitle)
    return (cleanedText, afterTitle)


def get_pageText(url):
    """
    Gets only pageText from url using BeautifulSoup and urlAnalyzer.
    Requires recreation of BeautifulSoup() object so don't call in
    htmlAnalyzer.py.
    """
    rawString = url_to_pageString(url)
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
    linkList = [link['href'] for link in a_list if parsable(link['href'])]
    return linkList


def detect_language(pageString):
    """ Detects language of a pageString """
    lang, score = langid.classify(pageString)
    return lang

try:
    d2vModel = BertClient(check_length=False)
except:
    print('WARNING: BertClient has not been initialized. This will affect srape_url functionality.')

# load classification models
newsClassifier = load_model('data/outData/binning/newsClassifier.sav')

def scrape_url(url, knowledgeProcessor, freqDict, timeout=10):
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
    rawString = url_to_pageString(url, timeout=timeout)
    loadEnd = time.time()

    ### PROCESS TIMES ###
    # round time page took to load to 10ths
    loadTime = round(loadEnd - loadStart, ndigits=1)
    # number of days since 1970 when page was loaded
    loadDate = int(loadEnd / (86400))

    ### CREATE SOUP OBJECT ###
    curSoup = BeautifulSoup(rawString, 'html.parser')

    ### GET TITLE AND CLEANED TEXT ###
    title = curSoup.title.string
    cleanedText, afterTitle = clean_pageText(curSoup.get_text(), title)
    cleanedTitle = clean_title(title)

    ### VALIDATE LANGUAGE ###
    assert (detect_language(cleanedText)=='en'), f"{url} contents not in English"

    ### FIND HEADERS ###
    h1Raw =         curSoup.find_all(h1Matcher)
    h2Raw =         curSoup.find_all(h2Matcher)
    h3Raw =         curSoup.find_all(h3Matcher)
    lowHeaderRaw =  curSoup.find_all(lowHeaderMatcher)
    # join cleaned headers into space delimited string
    h1Clean =           " ".join(str(header) for header in h1Raw)
    h2Clean =           " ".join(str(header) for header in h2Raw)
    h3Clean =           " ".join(str(header) for header in h3Raw)
    lowHeaderClean =    " ".join(str(header) for header in lowHeaderRaw)

    ### FIND META DESCRIPTION ###
    try:
        description = curSoup.find('meta', attrs={'name': 'description'}).get('content')
    except:
        description = ""

    ### FIND META KEYWORDS ###
    try:
        keywords = curSoup.find('meta', attrs={'name':'keywords'}).get('content')
    except:
        keywords = ""

    ### FIND IMAGES ALT TAGS ###
    try:
        images = curSoup.find_all('img')
        imageAlts = " ".join(img['alt'] for img in images)
        imageNum = len(images)
    except:
        imageAlts = ""

    ### ANALYZE AND SCORE KNOWLEDGE TOKENS ###
    divDict = {'url':           clean_url(url),
                'title':        cleanedTitle,
                'h1':           clean_text(h1Clean),
                'h2':           clean_text(h2Clean),
                'h3':           clean_text(h3Clean),
                'lowHeaders':   clean_text(lowHeaderClean),
                'description':  clean_text(description),
                'keywords':     clean_text(keywords),
                'imageAlt':     clean_text(imageAlts),
                'all':          cleanedText}

    # find dict mapping knowledge tokens in divDict to their score
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)

    ### FIND LINKS ###
    linkList = list(map(lambda url : fix_url(url), get_links(curSoup)))

    ### SET WINDOW TEXT TO DISPLAY ###
    windowText = description if not (description=="") else afterTitle

    ### VECTORIZE DOCUMENT ###
    pageVec = d2vModel.encode([afterTitle])[0]
    vecDF = pd.DataFrame(dv.docVec_to_dict(pageVec), index=[1])

    ### RUN CLASSIFIERS ON VECTOR ENCODING ###
    newsScore = newsClassifier.predict(vecDF)
    isNews = True if newsScore > 0.8 else False


    ### RETURN PAGE LIST ### imageNum
    return [url, cleanedTitle, knowledgeTokens, pageVec, linkList, loadTime, loadDate, windowText]
