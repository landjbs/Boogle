import numpy as np
from keras.models import load_model
from models.binning.docVecs import vectorize_doc
from crawlers.crawlLoader import load_crawled_pages

paraModel = load_model('data/outData/searchAnalysis/paragraphAnswering2.sav')
formatModel = load_model('data/outData/searchAnalysis/questionFormatModel.sav')

database, uniqueWords, searchProcessor = load_crawled_pages('data/thicctable/wikiCrawl4')
freqDict = load('data/outData/knowledge/freqDict.sav')

calc_score_activation = lambda freq : (1/freq)

while True:
    # vectorize search and get important tokens
    search = input('Search: ')
    searchVec = vectorize_doc(search)
    tokenScores = [(calc_score_activation(freqDict[token][0]), token)
                    for token in tokenSet]

    # find top pages
    importantToken = max(tokenScores, key=(lambda elt:elt[0]))[1]
    print(importantToken)

    pageList = database.search_pageObj(importantToken, n=3)

    # analyze question format
    formatPrediction = formatModel.predict(np.expand_dims(searchVec, axis=0))
    questionFormat =  True if (formatPrediction[0][0]>0.6) else False

    if quesitonFormat:
        topPage = pageList[0]
        topText = topPage.windowText
        textWords = topText.split()
        midWord = len(textWords) / 2
        paraList =  [topText[:midWord], topText[midWord:]]
        scoreList = [(paraModel.predict(np.expand_dims(np.subtract(searchVec, vectorize_doc(para)), axis=0)), para)
                        for para in paraList]
        print(max(scoreList)[1])
        
    else:
        dispList = [page.display([importantToken]) for page in pageList]
