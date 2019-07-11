from time import time

from dataStructures.pageObj import Page
from dataStructures.thicctable import Thicctable
from models.knowledge.knowledgeFinder import score_divDict
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor



knowledgeSet = {'the', 'discovered', 'harvard'}
database = Thicctable(knowledgeSet)
knowledgeProcessor = build_knowledgeProcessor(knowledgeSet)
freqDict = {token:0 for token in knowledgeSet}

filePath = 'data/inData/wikipedia_utf8_filtered_20pageviews.csv'

def make_wiki_url(title):
    """ Converts wikipedia title to url for the page """
    urlTitle = '_'.join(word for word in title.split())
    url = f'https://en.wikipedia.org/wiki/{urlTitle}'
    return url


with open(filePath, 'r') as wikiCsv:
    for i, line in enumerate(wikiCsv):
        # number of days since June 29 2019 when page was loaded
        loadDate = int(time() / (86400)) - 18076
        # get everything after the first comma
        rawText = line[21:]
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
                    'title':    title,
                    'all':      articleText}
        knowledgeTokens = score_divDict(divDict, knowledgeProcessor, freqDict)
        # determine text to show for the window
        windowText = title
        # build page object of article attributes
        pageObj = Page({'url':              url,
                        'title':            title,
                        'knowledgeTokens':  knowledgeTokens,
                        'pageVec':          {},
                        'linkList':         [],
                        'loadTime':         0.5,
                        'loadDate':         loadDate,
                        'imageScore':       0,
                        'videoScore':       0,
                        'windowText':       windowText})
        # bucket page object
        database.bucket_page(pageObj)

        print(f'\tCrawling: {i}', end='\r')

database.sort_all()

while True:
    search = input('Search: ')
    resultsList = (database.search_display(search, [search]))[:20]
    for result in resultsList:
        print(f'\t{result[1]}\n\t\t{result[0]}\n\t\t{result[2]}')









pass
