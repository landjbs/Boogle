from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method=='GET':
        print('get')
        return ('<form action="submit"><fieldset><legend>Personal information:</legend>First name:<br><input type="text" name="firstname" value="Mickey"><br>Last name:<br><input type="text" name="lastname" value="Mouse"><br><br><input type="submit" value="Submit"></fieldset></form>')
    else:
        print('post')
        result = request.form
        print(result)
