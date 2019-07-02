"""
Responsible for gathering and processing data from HTML pageStrings.
pageStrings generally passed from crawler.py after being cleaned by
urlAnalyzer.py. Outsources all NLP and ML to backend/models.
Bulkiest function is scrape_url which takes in a url and returns a
page object of page info.
"""

import re # to match for patterns in pageStrings
import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup # to parse html

from crawlers.urlAnalyzer import fix_url, url_to_pageString, parsable
from models.processing.cleaner import clean_text, clean_title, clean_url
from models.knowledge.knowledgeFinder import score_divDict
from models.binning.classification import classify_page
from models.binning.docVecs import vectorize_all
from models.ranking.baseRanker import calc_base_score

# matchers for header tags in html text
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
    # number of days since June 29 2019 when page was loaded
    loadDate = int(loadEnd / (86400)) - 18076

    ### CREATE SOUP OBJECT ###
    curSoup = BeautifulSoup(rawString, 'html.parser')

    ### GET TITLE AND CLEANED TEXT ###
    title = curSoup.title.string
    cleanedText, afterTitle = clean_pageText(curSoup.get_text(), title)
    cleanedTitle = clean_title(title)

    ### VALIDATE LANGUAGE ###
    assert (detect_language(cleanedText)=='en'), f"{url} contents not in English"

    ### FIND HEADERS AND CAST AS CLEAN STRING ###
    h1Raw =         " ".join(str(header) for header in curSoup.find_all(h1Matcher))
    h2Raw =         " ".join(str(header) for header in curSoup.find_all(h2Matcher))
    h3Raw =         " ".join(str(header) for header in curSoup.find_all(h3Matcher))
    lowHeaderRaw =  " ".join(str(header) for header in curSoup.find_all(lowHeaderMatcher))

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

    ### FIND VIDEO ALT TAGS: TO COMPLETE !!!! ###
    try:
        videos = curSoup.find('')
        videoAlts = ""
    except:
        videoAlts = ""

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
    linkList = list(map(lambda url:fix_url(url), get_links(curSoup)))

    ### SET WINDOW TEXT TO DISPLAY ###
    windowText = description if not (description=="") else afterTitle
    windowText = "No Information Availiable For This Page" if (windowText=="") else windowText

    ### VECTORIZE AND CLASSIFY DOCUMENT ###
    pageVec = vectorize_all(afterTitle)
    category = classify_page(pageVec)

    ### CALC BASE SCORE OF PAGE ###
    baseScore = calc_base_score(loadTime)

    ### RETURN PAGE LIST ### imageNum
    return [url, cleanedTitle, knowledgeTokens, pageVec, linkList, loadTime, loadDate, windowText]
