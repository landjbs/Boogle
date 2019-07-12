from time import time
from termcolor import colored
from os import listdir

from crawlers.wikiCrawler import crawl_wiki_data
from dataStructures.objectSaver import load, save
from dataStructures.pageObj import Page
from dataStructures.thicctable import Thicctable
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor
from searchers.searchLexer import topSearch
from models.knowledge.knowledgeFinder import find_rawTokens, score_divDict


crawl_wiki_data('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'data/thicctable/wikiCrawl', 100, 10)


print(colored('Loading Knowledge Set', 'red'), end='\r')
knowledgeSet = load('data/outData/knowledge/knowledgeSet.sav')
print(colored('Complete: Loading Knowledge Set', 'cyan'))

database = Thicctable(knowledgeSet)
del knowledgeSet

for i, file in enumerate(listdir('data/thicctable/wikiCrawl')):
    try:
        pagesList = load(f'data/thicctable/wikiCrawl/{file}')
        for pageDict in pagesList:
            pageObj = Page(pageDict)
            database.bucket_page(pageObj)
        print(colored(f'Building Database: {i}', 'red'), end='\r')
        del pagesList
    except Exception as e:
        print(f"{e} at '{file}'")
print(colored('Complete: Building Database', 'cyan'))

print(colored('Cleaning Database', 'red'), end='\r')
database.kill_empties()
print(colored('Complete: Cleaning Database', 'cyan'))

# sort the database
print(colored('Sorting Database', 'red'), end='\r')
database.sort_all()
print(colored('Complete: Sorting Database', 'cyan'))

# get dict mapping token to length of posting list
print(colored('Finding Posting Lengths', 'red'), end='\r')
# WORDS = database.all_lengths()
WORDS = {token:1 for token in ['harvard', 'college', 'university', 'radio', 'station', 'harvard college', 'harvard university', 'harvard radio', 'radio station']}
print(colored('Complete: Finding Posting Lengths', 'cyan'))

searchProcessor = build_knowledgeProcessor(WORDS)

print(f"\n{'-'*80}\nWelcome to Boogle Wikipedia DeNerf!")
while True:
    # get search text from user
    search = input('Search: ')
    # pass search, databse, and word info to topSearch
    try:
        start = time()
        correctionDisplay, resultsList = topSearch(search, database, searchProcessor, WORDS)
        end = time()
        # display formated results
        displayString = "<u>Boogle Wikipedia DeNerf</u><br>"
        displayString += f"{round(len(resultsList), 2)} results found in {end - start} seconds.<br>"
        if not (correctionDisplay==search):
            displayString += f"Showing results for <u>{correctionDisplay}</u>. Search instead for <a>{search}</a>.<br>"
        for result in resultsList:
            displayString += f'<br><strong>{result[1]}</strong><br><i>{result[0]}</i><br>{result[2]}<br>'
        print(displayString)
    except Exception as e:
        print(colored(f'ERROR: {e}', 'red'))









pass
