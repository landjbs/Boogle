from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        return render_template('index.html')
    else:
        query = request.form.get('home-search')
        return(query)
