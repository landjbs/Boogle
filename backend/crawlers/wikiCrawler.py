from time import time
from termcolor import colored
from queue import Queue
from threading import Thread

from dataStructures.objectSaver import load, save
from dataStructures.scrapingStructures import Simple_List, Metrics
from models.knowledge.knowledgeFinder import score_divDict
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor


def make_wiki_url(title):
    """ Converts wikipedia title to url for the page """
    urlTitle = '_'.join(word for word in title.split())
    url = f'https://en.wikipedia.org/wiki/{urlTitle}'
    return url


def scrape_wiki_page(line, knowledgeProcessor, freqDict):
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
    # build link of the webpage
    url = make_wiki_url(title)
    # build divDict and analyze for knowledgeTokens
    divDict = {'url':       url,
                'h3':       title,
                'all':      articleText}
    knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)
    # determine text to show for the window
    windowText = articleText[:400]
    # build and return pageDict of article attributes
    pageDict = {'url':              url,
                'title':            title,
                'knowledgeTokens':  knowledgeTokens,
                'pageVec':          {},
                'linkList':         [],
                'loadTime':         0.5,
                'loadDate':         loadDate,
                'imageScore':       0,
                'videoScore':       0,
                'windowText':       windowText}
    return(pageDict)


def crawl_wiki_data(inPath, outPath, queueDepth, workerNum):
    """
    Crawls cleaned wikipedia data at file path
    and saves page data to files under outPath
    """
    # load freqDict
    print(colored('Loading Freq Dict', 'red'), end='\r')
    freqDict = load('data/outData/knowledge/freqDict.sav')
    print(colored('Complete: Loading Freq Dict', 'cyan'))
    # load knowledgeProcessor
    print(colored('Loading Knowledge Processor', 'red'), end='\r')
    knowledgeProcessor = load('data/outData/knowledge/knowledgeProcessor.sav')
    print(colored('Complete: Loading Knowledge Processor', 'cyan'))

    # Queue to store lines from wiki file
    lineQueue = Queue(maxsize=queueDepth)
    # Simple_List to store pageDicts
    scrapeList = Simple_List()
    # Metrics to store scraping info
    scrapeMetrics = Metrics()

    def worker():
        """
        Scrapes popped wiki line from lineQueue and
        stores data in scrapeList
        """
        while True:
            line = lineQueue.get()
            try:
                pageDict = scrape_wiki_page(line, knowledgeProcessor, freqDict)
                scrapeList.add(pageDict)
                scrapeMetrics.add(error=False)
            except Exception as e:
                print(f"ERROR: {e}")
                scrapeMetrics.add(error=True)

            if (len(scrapeList.data)>=5):
                save(scrapeList.data, f'{outPath}/{scrapeMetrics.count}.sav')
                scrapeList.clear()

            queueSize = lineQueue.qsize()
            print(f'Pages Analyzed: {scrapeMetrics.count} | Errors: {scrapeMetrics.errors} | Queue Length: {queueSize}', end='\r')
            lineQueue.task_done()

    # spawn workerNum workers
    for _ in range(workerNum):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # load wiki lines into lineQueue
    with open(inPath, 'r') as wikiFile:
        for line in wikiFile:
            lineQueue.put(line)
    print('\nScraping Complete')
    return True
