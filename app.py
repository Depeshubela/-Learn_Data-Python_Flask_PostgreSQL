import flask
from flask import Flask, url_for, redirect,render_template,request
from datetime import datetime

app = Flask(__name__)

@app.route("/") 
def login():

    return render_template('abc.html')

if __name__ == '__main__':
    app.debug = True
    app.run()    