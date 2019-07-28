import numpy as np
from keras.models import load_model
from dataStructures.objectSaver import load
# from models.binning.docVecs import vectorize_doc
from crawlers.crawlLoader import load_crawled_pages

# paraModel = load_model('data/outData/searchAnalysis/paragraphAnswering2.sav')
# formatModel = load_model('data/outData/searchAnalysis/questionFormatModel.sav')
#
# database, uniqueWords, searchProcessor = load_crawled_pages('data/thicctable/wikiCrawl4')
# freqDict = load('data/outData/knowledge/freqDict.sav')

paraList = []

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i > 0:
            break
        commaLoc = line.find(',')
        para = line[commaLoc:]
        chunkSize = int(len(para) / 4)
        chunkStart = 0
        for chunkEnd in range(0, len(para), chunkSize):
            if not chunkEnd==0:
                paraList.append(para[chunkStart:chunkEnd])
            chunkStart = chunkEnd

paraVecs = [np.expand_dims(vectorize_doc(para), axis=0)
            for para in paraList]

while True:
    search = input('Search: ')
    searchVec = np.expand_dims(vectorize_doc(search), axis=0)
    questionFormat = True if (formatModel.predict(searchVec)>=0.6) else False
    if questionFormat:
        distList = [paraModel.predict(np.expand_dims(np.subtract(searchVec, paraVec), axis=0))
                    for paraVec in paraVecs]
        distList.sort(reverse=True)
        print(distList[0][0])
    else:
        print('keyword')
