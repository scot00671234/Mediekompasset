from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import nltk
from transformers import pipeline

# Download required NLTK data at startup
try:
    nltk.download('punkt', quiet=True)
except Exception as e:
    print(f"NLTK download error (non-critical): {str(e)}")

app = Flask(__name__)
CORS(app)

# Initialize model globally
try:
    classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
except Exception as e:
    print(f"Model loading error (will retry on demand): {str(e)}")
    classifier = None

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    global classifier
    try:
        # Test NLTK
        nltk.tokenize.word_tokenize("Test sentence")
        
        # Test transformer model
        if classifier is None:
            classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
        test_result = classifier("Test sentence")[0]
        
        return jsonify({
            "status": "healthy",
            "nltk_test": "passed",
            "transformer_test": "passed",
            "model_loaded": True
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
