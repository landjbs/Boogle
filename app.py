import sys
from time import time
from flask import Flask, flash, jsonify, redirect, render_template, request, session
sys.path.append("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend")

from crawlers.crawlLoader import load_crawled_pages
from searchers.searchLexer import topSearch

app = Flask(__name__)

database, uniqueWords, searchProcessor = load_crawled_pages('backend/data/thicctable/wikiCrawl2')

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        rawSearch = request.form.to_dict()['Search']
        # perform search and gather searchStats
        searchStart = time()
        correctionDisplay, resultList = topSearch(rawSearch, database, uniqueWords, searchProcessor)
        searchTime = round((time() - searchStart), 4)
        searchStats = (len(resultList), searchTime)
        # return search info
        return render_template('result.html', searchStats=searchStats, correctionDisplay=correctionDisplay, resultList=resultList)
    elif request.method == 'GET':
        ## Fix to render the page that was clicked on and save the info ##
        pass
