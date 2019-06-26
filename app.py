import sys
sys.path.append("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend")

from topLevel import flask_search

from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        searchStats, correctionDisplay, resultList = flask_search(request.form.to_dict()['Search'])
        return render_template('result.html', searchStats=searchStats, correctionDisplay=correctionDisplay, resultList=resultList)
    elif request.method == 'GET':
        ## Fix to render the page that was clicked on and save the info ##
        pass
