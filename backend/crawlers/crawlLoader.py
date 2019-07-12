"""
Loads files that have been crawled into a thicctable
"""
from os import listdir
from termcolor import colored

from dataStructures.objectSaver import load, save
from dataStructures.pageObj import Page
from dataStructures.thicctable import Thicctable

def load_crawled_pages(filePath):
    """
    Loads crawled pages under filePath into a Thicctable().
    Returns:
        -database:          Thicctable() obj of page data
        -words:             set of the unique words of token buckets in
                            the database and their lengths
        -searchProcessor:   knowledgeProcessor to find words in database
    """
    # initialize database with knowledgeSet buckets
    print(colored('Loading Knowledge Set', 'red'), end='\r')
    knowledgeSet = load('data/outData/knowledge/knowledgeSet.sav')
    print(colored('Complete: Loading Knowledge Set', 'cyan'))
    database = Thicctable(knowledgeSet)
    del knowledgeSet
    # bucket each page in each file in filePath
    for i, file in enumerate(listdir(filePath)):
        try:
            pageList = load(f'{filePath}/{file}')
            for pageDict in pageList:
                databse.bucket_page(Page(pageDict))
            print(colored(f'Building Database: {i}', 'red'), end='\r')
        except Exception as e:
            print(f'{e} at "{file}".')
    print(colored('Complete: Building Database', 'cyan'))
    # clean and sort the database
