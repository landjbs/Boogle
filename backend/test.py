from time import time

from os import listdir

from crawlers.crawlLoader import load_crawled_pages
from searchers.searchLexer import topSearch


database, uniqueWords, searchProcessor = load_crawled_pages('data/thicctable/wikiCrawl')

print(f"\n{'-'*80}\nWelcome to Boogle Wikipedia DeNerf!")
while True:
    # get search text from user
    search = input('Search: ')
    # pass search, databse, and word info to topSearch
    try:
        start = time()
        correctionDisplay, resultsList = topSearch(search, database, searchProcessor, uniqueWords)
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
