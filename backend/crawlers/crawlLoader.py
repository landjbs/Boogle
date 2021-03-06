"""
Loads files that have been crawled into a thicctable
"""

from math import inf
from tqdm import tqdm
from os import listdir
from termcolor import colored

from dataStructures.objectSaver import load, save
from dataStructures.pageObj import Page
from dataStructures.thicctable import Thicctable
from models.knowledge.knowledgeBuilder import build_knowledgeProcessor


def load_crawled_pages(filePath, n=inf, loadProcessor=True):
    """
    Loads crawled pages under filePath into a Thicctable().
    Returns:
        -database:          Thicctable() obj of page data
        -uniqueWords:       set of the unique words of token buckets in
                            the database and their lengths
        -searchProcessor:   knowledgeProcessor to find words in database
    """
    # initialize database with knowledgeSet buckets and corrDict relatedTokens
    print(colored('Loading Knowledge Set', 'red'), end='\r')
    # knowledgeSet = load('backend/data/outData/knowledge/knowledgeSet.sav')
    knowledgeSet = {}
    print(colored('Complete: Loading Knowledge Set', 'cyan'))

    print(colored('Loading Corr Dict', 'red'), end='\r')
    corrDict = load('backend/data/outData/knowledge/corrDict.sav')
    corrDict.update({token:[] for token in knowledgeSet
                        if not token in corrDict})
    del knowledgeSet
    print(colored('Complete: Loading Corr Dict', 'cyan'))

    # build database, using corrDict to get keys and relatedTokens
    database = Thicctable(corrDict)
    del corrDict

    # bucket each page in each file in filePath
    for i, file in enumerate(tqdm(listdir(filePath))):
        if i > n:
            break
        try:
            pageList = load(f'{filePath}/{file}')
            for pageDict in pageList:
                database.bucket_page(Page(pageDict))
        except Exception as e:
            print(f'{e} at "{file}".')
    print(colored('Complete: Building Database', 'cyan'))

    # clean and sort the database
    print(colored('Cleaning Database', 'red'), end='\r')
    database.kill_empties()
    # print(colored('Complete: Cleaning Database', 'cyan'))
    print(colored('Sorting Database', 'red'), end='\r')
    database.sort_all()
    print(colored('Complete: Sorting Database', 'cyan'))
    # find all unique, non-empty words in the database and the length of their posting list
    print(colored('Finding Unique Words', 'red'), end='\r')

    database.initialize_relevances()

    # nonemptyTokens = database.all_lengths()
    # print(f'\n\n{"-"*80}\nNonempty:\n{nonemptyTokens}\n{"-"*80}\n\n')
    # uniqueWords = nonemptyTokens.copy()
    # for token, length in nonemptyTokens.items():
    #     words = token.split()
    #     for word in words:
    #         if not word in nonemptyTokens:
    #             uniqueWords.update({word:length})
    uniqueWords = database.all_relevances()

    print(colored('Complete: Finding Unique Words', 'cyan'))
    # flashtext processor to find keywords in search
    print(colored('Loading Processor', 'red'), end='\r')
    if loadProcessor:
        searchProcessor = load('backend/data/outData/knowledge/knowledgeProcessor.sav')
    else:
        searchProcessor = build_knowledgeProcessor(uniqueWords)
    print(colored('Complete: Loading Processor', 'cyan'))

    return(database, uniqueWords, searchProcessor)
