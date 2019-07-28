from keras.models import load_model
from models.binning.docVecs import vectorize_doc
from crawlers.crawlLoader import load_crawled_pages

paragrapahModel = load_model('data/outData/searchAnalysis/paragraphAnswering2.sav')
formatModel = load_model('data/outData/searchAnalysis/questionFormatModel.sav')

database, uniqueWords, searchProcessor = load_crawled_pages('data/thicctable/wikiCrawl4')
freqDict = load('data/outData/knowledge/freqDict.sav')

calc_score_activation = lambda freq : (1/freq)

while True:
    # vectorize search and get important tokens
    search = input('Search: ')
    searchVec = vectorize_doc(search)
    tokenScores = {token : calc_score_activation(freqDict[token][0])
                    for token in tokenSet}
    # analyze question format
    formatPrediction = formatModel.predict(np.expand_dims(searchVec, axis=0))
    questionFormat =  True if (formatPrediction[0][0]>0.6) else False
    if quesitonFormat:
