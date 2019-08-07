import sys
sys.path.append("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend")

from dataStructures.objectSaver import load
from crawlers.crawlLoader import load_crawled_pages

database, uniqueWords, searchProcessor = load_crawled_pages('backend/data/thicctable/wikiCrawl4', n=10)
freqDict = load('backend/data/outData/knowledge/freqDict.sav')

from flask import Flask, render_template, request
from searchers.searchLexer import topSearch

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    print(request.remote_addr)
    if request.method == 'POST':
        rawSearch = request.form.to_dict()['Search']
        if (rawSearch==""):
            return render_template('index.html')
        # perform search and gather searchStats
        else:
            # correctionDisplay, numResults, invertedResult, resultList = topSearch(rawSearch, database, uniqueWords, searchProcessor, freqDict)
            resultObj = topSearch(rawSearch, database, uniqueWords, searchProcessor, freqDict)

            resultObj.log()

            # return search info
            # return render_template('result.html', searchStats=searchStats, correctionDisplay=correctionDisplay, invertedResult=invertedResult, resultList=resultList, searchWords=rawSearch.split())
            return render_template('result.html', resultObj=resultObj)
    elif request.method == 'GET':
        ## Fix to render the page that was clicked on and save the info ##
        pass
