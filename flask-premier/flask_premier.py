from flask import jsonify
from flask import request
from flask import Flask

def entry():
    app = Flask(__name__)
    return app

app = entry()

@app.route('/premier')
def get_number():
    number = request.args.get('number', default = 1, type = int)
    if (number % 2) == 0:
        return jsonify(pair=number)
    else:
        return jsonify(impair=number)

@app.route('/health')
def health():
    return 'ok'

@app.route('/ping')
def ping():
    return 'pong'