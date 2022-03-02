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
    API_URL = os.environ.get('PREMIER-API-URL')
    #return requests.get('http://flask-premier:33330/premier?number=' + str(number), verify=False).content
    # Stocker http://entry-test.info:30000/premier?number= dans configMap
    return requests.get(API_URL + str(number), verify=False).content

@app.route('/health')
def health():
    return 'ok'

@app.route('/ping')
def ping():
    return 'pong'
