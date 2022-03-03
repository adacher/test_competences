from flask import jsonify
from flask import request
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics

def entry():
    app = Flask(__name__)
    metrics = PrometheusMetrics(app)
    return app

app = entry()

@app.route('/premier')
def get_number():
    number = request.args.get('number', default = 1, type = int)
    if (number % 2) == 0:
        return jsonify(pair=number), 200
    else:
        return jsonify(impair=number), 200

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