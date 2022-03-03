import requests
from random import randrange
import os
from flask import jsonify
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

def entry():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    return app

app = entry()

@app.route('/random')
def random_number():
    number = randrange(10000)
    API_URL = os.environ.get('PREMIER-API-URL')
    return requests.get(API_URL + str(number), verify=False).content

@app.route('/health')
def health():
    json = {
            'health' : 'ok'
        }
    return json, 200

@app.route('/ping')
def ping():
    json = {
            'ping' : 'pong'
        }
    return json, 200