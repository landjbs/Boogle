from math import inf
from time import time
from tqdm import tqdm
from termcolor import colored
from collections import Counter

from models.ranking.baseRanker import calc_base_score
from models.processing.cleaner import clean_text
# from models.binning.docVecs import vectorize_doc
from models.knowledge.knowledgeFinder import score_divDict
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from dataStructures.scrapingStructures import Simple_List
from dataStructures.objectSaver import load, save, safe_make_folder


def make_wiki_url(title):
    """ Converts wikipedia title to url for the page """
    urlTitle = '_'.join(word for word in title.split())
    url = f'https://en.wikipedia.org/wiki/{urlTitle}'
    return url


def add_shadow_tokens(knowledgeTokens, corrDict, cutoff=0.2):
    """
    UNDER DEVELOPMENT: Adds shadow tokens to knowlegeTokens by merging
    related token lists
    """
    relCounts = Counter()
    for knowledgeToken, knowledgeScore in knowledgeTokens.items():
        if knowledgeToken in corrDict:
            relatedTokens = corrDict[knowledgeToken]
            for relatedScore, relatedToken in relatedTokens:
                weightedScore = knowledgeScore * relatedScore
                if weightedScore > cutoff:
                    relCounts.update({relatedToken : weightedScore})
    # update knowledgeTokens
    knowledgeCounter = Counter(knowledgeTokens)
    return knowledgeCounter


def scrape_wiki_page(line, knowledgeProcessor, freqDict, corrDict):
    """ Scrapes line (page) from wikipedia csv and returns pageDict """
    # number of days since June 29 2019 when page was loaded
    loadDate = int(time() / (86400)) - 18076
    # get everything after the first comma
    commaLoc = line.find(',')
    rawText = line[(commaLoc+2):]
    # pull out the title
    titleEnd = rawText.find('  ')
    title = rawText[:titleEnd]
    # get the article text and strip whitespace
    articleText = rawText[(titleEnd+2):]
    articleText = articleText.strip()
    # clean the articleText
    cleanedText = clean_text(articleText)
    # build link of the webpage
    url = make_wiki_url(title)
    # build divDict and analyze for knowledgeTokens
    divDict = {'url':       url,
                'h3':       title,
                'all':      cleanedText}
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)
    knowledgeTokens = add_shadow_tokens(knowledgeTokens, corrDict, cutoff=0.2)
    # vectorize the article text
    # pageVec = vectorize_doc(articleText)
    pageVec = {}
    # create dict of base attributes of the page and score
    baseAttributes = {'loadTime': 0.5, 'imageScore':0, 'videoScore':0}
    baseScore = calc_base_score(baseAttributes)
    # determine text to show for the window
    windowText = articleText
    # build and return pageDict of article attributes
    pageDict = {'url':              url,
                'title':            title,
                'knowledgeTokens':  knowledgeTokens,
                'pageVec':          pageVec,
                'linkList':         [],
                'loadDate':         loadDate,
                'baseScore':        baseScore,
                'windowText':       windowText}
    return(pageDict)


def crawl_wiki_data(inPath, outPath, startNum=None, endNum=None):
    """
    Crawls cleaned wikipedia data at file path
    and saves page data to files under outPath
    """

    safe_make_folder(outPath)

    # load freqDict
    print(colored('Loading Freq Dict', 'red'), end='\r')
    freqDict = load('data/outData/knowledge/freqDict.sav')
    print(colored('Complete: Loading Freq Dict', 'cyan'))
    # load corrDict
    print(colored('Loading Corr Dict', 'red'), end='\r')
    corrDict = load('data/outData/knowledge/relationshipDict.sav')
    print(colored('Complete: Loading Corr Dict', 'cyan'))
    # load knowledgeProcessor
    print(colored('Loading Knowledge Processor', 'red'), end='\r')
    knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
    print(colored('Complete: Loading Knowledge Processor', 'cyan'))

    # Simple_List to store pageDicts
    scrapeList = Simple_List()

    if not startNum:
        startNum = 0
    if not endNum:
        endNum = inf

    with open(inPath, 'r') as wikiFile:
        for i, line in enumerate(tqdm(wikiFile)):
            if i > endNum:
                break
            if i >= startNum:
                try:
                    pageDict = scrape_wiki_page(line,
                                                knowledgeProcessor,
                                                freqDict,
                                                corrDict)
                    scrapeList.add(pageDict)
                except Exception as e:
                    print(f"ERROR: {e}")

                if (len(scrapeList.data)>=3):
                    save(scrapeList.data, f'{outPath}/{i}.sav')
                    scrapeList.clear()

    if (scrapeList.data != []):
        save(scrapeList.data, f'{outPath}/{i}.sav')

    print('\n\nScraping Complete\n')
    return True
