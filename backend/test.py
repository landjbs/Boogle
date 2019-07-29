# import searchers.modelBuilders.paragraphFinding as pf
import re
import numpy as np
from keras.models import load_model
from dataStructures.objectSaver import load
from models.binning.docVecs import vectorize_doc
from tqdm import tqdm
# from crawlers.crawlLoader import load_crawled_pages

paraModel = load_model('data/outData/searchAnalysis/paragraphAnswering2.sav')
formatModel = load_model('data/outData/searchAnalysis/questionFormatModel.sav')

paraList = []

with open('data/inData/wikipedia_utf8_filtered_20pageviews.csv', 'r') as wikiFile:
    for i, line in enumerate(wikiFile):
        if i > 0:
            break
        commaLoc = line.find(',')
        para = line[commaLoc:]
        # chunkSize = int(len(para) / 4)
        # chunkStart = 0
        # for chunkEnd in range(0, len(para), chunkSize):
        #     if not chunkEnd==0:
                # paraList.append(para[chunkStart:chunkEnd])
                # chunkStart = chunkEnd
        for chunk in re.split(r'[.\?!]', para):
            print(chunk)
            paraList.append(chunk)

paraVecs = {para:np.expand_dims(vectorize_doc(para), axis=0)
            for para in tqdm(paraList)}

while True:
    search = input('Search: ')
    searchVec = np.expand_dims(vectorize_doc(search), axis=0)
    formatPrediction = formatModel.predict(searchVec)
    print(formatPrediction)
    questionFormat = True if (formatPrediction>=0.5) else False
    if questionFormat:
        distList = [(paraModel.predict(np.subtract(searchVec, paraVec)), paraText)
                    for paraText, paraVec in paraVecs.items()]
        distList.sort(reverse=True)
        print(distList)
        print(distList[0][1])
    else:
        print('keyword')
