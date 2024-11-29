from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

def application(environ, start_response):
    with app.request_context(environ):
        response = app.dispatch_request()
        status = f'{response.status_code} {response.status}'
        response_headers = [(k, v) for k, v in response.headers.items()]
        start_response(status, response_headers)
        return [response.get_data()]
