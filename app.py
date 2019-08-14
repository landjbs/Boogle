from sys import path
path.append("/Users/landonsmith/Desktop/DESKTOP/Code/personal-projects/search-engine/backend")

from flask import Flask, render_template, request

from searchers.searchLexer import topSearch
from dataStructures.userObj import User

app = Flask(__name__)

# test
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        rawSearch = request.form.to_dict()['Search']
        if (rawSearch==""):
            return render_template('index.html')
        # perform search and gather searchStats
        else:
            user = User(ip=request.remote_addr)
            resultObj = topSearch(rawSearch=rawSearch,
                                    user=user)

            resultObj.log()

            # return search info
            return render_template('result.html', resultObj=resultObj)

    elif request.method == 'GET':
        ## Fix to render the page that was clicked on and save the info ##
        pass
