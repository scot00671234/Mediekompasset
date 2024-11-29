from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import nltk

# Download required NLTK data at startup
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"NLTK download error (non-critical): {str(e)}")

app = Flask(__name__)
CORS(app)

# Removed transformer-based classifier

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    try:
        # Test NLTK
        nltk.tokenize.word_tokenize("Test sentence")
        
        return jsonify({
            "status": "healthy",
            "nltk_test": "passed"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
