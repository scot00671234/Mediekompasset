from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import nltk
import re

# Download required NLTK data at startup
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except Exception as e:
    print(f"NLTK download error (non-critical): {str(e)}")

app = Flask(__name__)
CORS(app)

# Simple sentiment lexicon
POSITIVE_WORDS = {'good', 'great', 'excellent', 'positive', 'awesome', 'fantastic', 'wonderful', 'amazing'}
NEGATIVE_WORDS = {'bad', 'terrible', 'awful', 'negative', 'poor', 'horrible', 'worst', 'disappointing'}

def simple_sentiment_analysis(text):
    """
    Perform a basic sentiment analysis using word matching.
    
    Args:
        text (str): Input text to analyze
    
    Returns:
        dict: Sentiment analysis result with label and score
    """
    # Lowercase and tokenize
    words = set(re.findall(r'\w+', text.lower()))
    
    # Count sentiment words
    positive_count = len(words.intersection(POSITIVE_WORDS))
    negative_count = len(words.intersection(NEGATIVE_WORDS))
    
    # Determine sentiment
    if positive_count > negative_count:
        return {"label": "POSITIVE", "score": positive_count / (positive_count + negative_count)}
    elif negative_count > positive_count:
        return {"label": "NEGATIVE", "score": negative_count / (positive_count + negative_count)}
    else:
        return {"label": "NEUTRAL", "score": 0.5}

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

@app.route('/api/sentiment', methods=['POST'])
def sentiment_analysis():
    """
    Endpoint for sentiment analysis
    """
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        result = simple_sentiment_analysis(text)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    try:
        # Test NLTK
        nltk.tokenize.word_tokenize("Test sentence")
        
        # Test sentiment analysis
        test_sentiment = simple_sentiment_analysis("This is a great day!")
        
        return jsonify({
            "status": "healthy",
            "nltk_test": "passed",
            "sentiment_test": test_sentiment
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
