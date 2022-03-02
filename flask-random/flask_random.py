import requests
from random import randrange
import os
from flask import jsonify
from flask import Flask

def entry():
    app = Flask(__name__)
    return app

app = entry()

@app.route('/random')
def random_number():
    number = randrange(10000)
    #return requests.get('http://flask-premier:33330/premier?number=' + str(number), verify=False).content
    return requests.get('http://192.168.59.101:30000/premier?number=' + str(number), verify=False).content

@app.route('/health')
def health():
    return 'ok'

@app.route('/ping')
def ping():
    return 'pong'
