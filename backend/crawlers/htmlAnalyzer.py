"""
Responsible for gathering and processing data from HTML pageStrings.
pageStrings generally passed from crawler.py after being cleaned by
urlAnalyzer.py. Outsources all NLP and ML to backend/models.
Bulkiest function is scrape_url which takes in a url and returns a
page object of page info.
"""

import re # to match for patterns in pageStrings
from time import time # to find the loadTime of a page
import langid # to classify language of pageString
from bs4 import BeautifulSoup # to parse html

from crawlers.urlAnalyzer import fix_url, url_to_pageString, parsable
import models.processing.cleaner as cleaner
from models.knowledge.knowledgeFinder import score_divDict
# from models.binning.classification import classify_page
# from models.binning.docVecs import vectorize_all
# from models.ranking.baseRanker import calc_base_score

# matchers for header tags in html text
h1Matcher = re.compile('^h1$')
h2Matcher = re.compile('^h2$')
h3Matcher = re.compile('^h3$')
lowHeaderMatcher = re.compile('^h[4-6$]')


def is_visible(element):
    """ Checks if html element is visible on a webpage """
    if element.parent.name in ['head', 'title', '[document]', 'style', 'script']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def clean_pageText(rawText, title):
    """
    Removes junk from output of soup.get_text()
    Returns: completely cleaned text and raw text with title removed
    """
    # find location of end of the title in rawText
    titleEnd = rawText.find(title) + len(title)
    # filter out everything before the title
    afterTitle = rawText[titleEnd:]
    # call clean_web_text from models.textProcessor.cleaner
    cleanedText = cleaner.clean_web_text(afterTitle)
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
    cleanedText, _ = clean_pageText(rawText, title)
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
    loadStart = time()
    rawString = url_to_pageString(url, timeout=timeout)
    loadEnd = time()

    ### PROCESS TIMES ###
    # round time page took to load to 10ths
    loadTime = round(loadEnd - loadStart, ndigits=1)
    # number of days since June 29 2019 when page was loaded
    loadDate = int(loadEnd / (86400)) - 18076

    ### CREATE SOUP OBJECT ###
    curSoup = BeautifulSoup(rawString, 'html.parser')

    ### GET TITLE AND CLEANED TEXT ###
    title = curSoup.title.string
    visible_text = ' '.join(filter(is_visible, curSoup.findAll(text=True)))
    cleanedText, afterTitle = clean_pageText(visible_text, title)
    cleanedTitle = cleaner.clean_title(title)

    ### VALIDATE LANGUAGE ###
    assert (detect_language(cleanedText)=='en'), f"{url} contents not in English"

    ### FIND HEADERS AND CAST AS CLEAN STRING ###
    h1 =         " ".join(str(header) for header in curSoup.find_all(h1Matcher))
    h2 =         " ".join(str(header) for header in curSoup.find_all(h2Matcher))
    h3 =         " ".join(str(header) for header in curSoup.find_all(h3Matcher))
    lowHeader =  " ".join(str(header) for header in curSoup.find_all(lowHeaderMatcher))

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
        imageScore = len(images)
        imageAlts = ""
        # build string of imageAlts
        for image in images:
            imageAlts += f" {image['alt']} "
            # doc imageScore by 0.5 if no image styling is given
            try:
                _, _ = image['height'], image['width']
            except:
                try:
                    _ = image['style']
                except:
                    imageScore -= 0.5
    except:
        imageScore, imageAlts = 0, ""

    ### FIND VIDEO ALT TAGS ###
    try:
        videos = curSoup.find('video')
        videoScore = len(videos)
        videoSRCs = " ".join(video['src'] for video in videos)
    except:
        videoScore, videoSRCs = 0, ""

    ### ANALYZE AND SCORE KNOWLEDGE TOKENS ###
    divDict = {'url':           cleaner.clean_url(url),
                'title':        cleanedTitle,
                'h1':           cleaner.clean_text(h1),
                'h2':           cleaner.clean_text(h2),
                'h3':           cleaner.clean_text(h3),
                'lowHeaders':   cleaner.clean_text(lowHeader),
                'description':  cleaner.clean_text(description),
                'keywords':     cleaner.clean_text(keywords),
                'imageAlts':    cleaner.clean_text(imageAlts),
                'videoSRCs':    cleaner.clean_file_name(videoSRCs),
                'all':          cleanedText}

    # find dict mapping knowledge tokens in divDict to their score
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)

    ### FIND LINKS ###
    linkList = list(map(lambda link:fix_url(link, url), get_links(curSoup)))

    ### SET WINDOW TEXT TO DISPLAY ###
    windowText = description if not (description=="") else afterTitle
    assert (windowText != ""), f"{url} has no windowText"

    ### VECTORIZE AND CLASSIFY DOCUMENT ###
    # pageVec = vectorize_all(afterTitle)
    # category = classify_page(pageVec)
    pageVec = {}
    category = 'news'

    ### CALC BASE SCORE OF PAGE ###
    # baseScore = calc_base_score(loadTime)

    ### RETURN PAGE LIST ### imageNum
    return [url, cleanedTitle, knowledgeTokens, pageVec, linkList, loadTime, loadDate, windowText]
