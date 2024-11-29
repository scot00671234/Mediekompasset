from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import nltk

app = Flask(__name__)
CORS(app)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({
        "status": "healthy"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
