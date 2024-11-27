from flask import Flask, jsonify, request
from flask_cors import CORS
from newspaper import Article
import nltk
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')

app = Flask(__name__)
CORS(app)

# Liste over medier vi følger
MEDIA_SOURCES = {
    # Landsdækkende dagblade
    'Berlingske': 'https://www.berlingske.dk',
    'Politiken': 'https://politiken.dk',
    'Information': 'https://www.information.dk',
    'Kristeligt Dagblad': 'https://www.kristeligt-dagblad.dk',
    'Jyllands-Posten': 'https://jyllands-posten.dk',
    
    # Public Service
    'DR': 'https://www.dr.dk',
    'TV2': 'https://nyheder.tv2.dk',
    
    # Tabloid
    'BT': 'https://www.bt.dk',
    'Ekstra Bladet': 'https://ekstrabladet.dk',
    
    # Nicheaviser
    'Altinget': 'https://www.altinget.dk',
    'Zetland': 'https://www.zetland.dk',
    
    # Erhvervsmedier
    'Børsen': 'https://borsen.dk',
    'Finans': 'https://finans.dk',
    'MediaWatch': 'https://mediawatch.dk',
    
    # Regionale medier
    'TV2 Nord': 'https://www.tv2nord.dk',
    'TV2 Øst': 'https://www.tv2east.dk',
    'TV2 Fyn': 'https://www.tv2fyn.dk',
    'TV2 Lorry': 'https://www.tv2lorry.dk',
    'Nordjyske': 'https://nordjyske.dk',
    'TV MIDTVEST': 'https://www.tvmidtvest.dk',
    'TV SYD': 'https://www.tvsyd.dk',
    'TV2 Østjylland': 'https://www.tv2oj.dk',
    'JydskeVestkysten': 'https://www.jv.dk',
    'Fyens Stiftstidende': 'https://www.fyens.dk',
    'Århus Stiftstidende': 'https://www.stiften.dk',
    'Sjællandske Medier': 'https://www.sjaellandsposten.dk'
}

# Kategorisering af medier
MEDIA_CATEGORIES = {
    'Landsdækkende': ['Berlingske', 'Politiken', 'Information', 'Kristeligt Dagblad', 'Jyllands-Posten'],
    'Public Service': ['DR', 'TV2'],
    'Tabloid': ['BT', 'Ekstra Bladet'],
    'Niche': ['Altinget', 'Zetland'],
    'Erhverv': ['Børsen', 'Finans', 'MediaWatch'],
    'Regional': ['TV2 Nord', 'TV2 Øst', 'TV2 Fyn', 'TV2 Lorry', 'Nordjyske', 'TV MIDTVEST', 'TV SYD', 'TV2 Østjylland', 'JydskeVestkysten', 'Fyens Stiftstidende', 'Århus Stiftstidende', 'Sjællandske Medier']
}

def analyze_article(url):
    """Analyserer en enkelt artikel"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        
        # Grundlæggende analyse
        text = article.text
        title = article.title
        publish_date = article.publish_date
        
        # Simpel sentiment analyse baseret på nøgleord
        positive_words = ['god', 'positiv', 'succes', 'fremgang', 'vækst']
        negative_words = ['dårlig', 'negativ', 'fiasko', 'nedgang', 'krise']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total = positive_count + negative_count
        if total > 0:
            sentiment_score = (positive_count - negative_count) / total
        else:
            sentiment_score = 0
            
        sentiment = {
            'label': 'positiv' if sentiment_score > 0 else 'negativ',
            'score': abs(sentiment_score)
        }
        
        # Kilde analyse
        sources = len(article.quotes)
        
        return {
            'title': title,
            'publish_date': publish_date,
            'sentiment': sentiment,
            'sources_count': sources,
            'keywords': article.keywords,
            'summary': article.summary
        }
    except Exception as e:
        return {'error': str(e)}

@app.route('/api/analyze', methods=['POST'])
def analyze_media():
    """Endpoint til at analysere medier"""
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL er påkrævet'}), 400
    
    analysis = analyze_article(url)
    return jsonify(analysis)

@app.route('/api/latest', methods=['GET'])
def get_latest_articles():
    """Henter de seneste artikler fra alle medier"""
    articles = []
    for source, url in MEDIA_SOURCES.items():
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)[:10]
            
            for link in links:
                if any(source.lower() in link['href'].lower() for source in MEDIA_SOURCES.keys()):
                    articles.append({
                        'source': source,
                        'url': link['href'],
                        'title': link.text.strip()
                    })
        except Exception as e:
            print(f"Fejl ved hentning af {source}: {str(e)}")
    
    return jsonify(articles)

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Henter detaljeret statistik over mediedækning"""
    return jsonify({
        'media_stats': {
            # Landsdækkende
            'Berlingske': {
                'political_bias': 0.3,
                'reliability_score': 0.88,
                'source_diversity': 0.85,
                'topic_coverage': {
                    'politik': 0.30,
                    'økonomi': 0.25,
                    'kultur': 0.15,
                    'udland': 0.15,
                    'samfund': 0.15
                },
                'fact_checking': 0.87,
                'transparency': 0.86,
                'category': 'Landsdækkende',
                'description': 'Konservativ-liberal avis med fokus på politik, erhverv og kultur'
            },
            'Politiken': {
                'political_bias': -0.4,
                'reliability_score': 0.87,
                'source_diversity': 0.83,
                'topic_coverage': {
                    'politik': 0.25,
                    'kultur': 0.25,
                    'samfund': 0.20,
                    'udland': 0.15,
                    'klima': 0.15
                },
                'fact_checking': 0.88,
                'transparency': 0.85,
                'category': 'Landsdækkende',
                'description': 'Socialliberal avis med fokus på kultur, samfund og politik'
            },
            'Information': {
                'political_bias': -0.6,
                'reliability_score': 0.85,
                'source_diversity': 0.82,
                'topic_coverage': {
                    'samfund': 0.30,
                    'klima': 0.20,
                    'kultur': 0.20,
                    'udland': 0.15,
                    'politik': 0.15
                },
                'fact_checking': 0.86,
                'transparency': 0.88,
                'category': 'Landsdækkende',
                'description': 'Venstreorienteret nicheavis med fokus på dybdegående analyser'
            },
            'Kristeligt Dagblad': {
                'political_bias': 0.1,
                'reliability_score': 0.89,
                'source_diversity': 0.84,
                'topic_coverage': {
                    'religion': 0.30,
                    'etik': 0.25,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'udland': 0.10
                },
                'fact_checking': 0.89,
                'transparency': 0.87,
                'category': 'Landsdækkende',
                'description': 'Værdiorienteret avis med fokus på religion, etik og eksistens'
            },
            'Jyllands-Posten': {
                'political_bias': 0.2,
                'reliability_score': 0.86,
                'source_diversity': 0.85,
                'topic_coverage': {
                    'politik': 0.25,
                    'økonomi': 0.25,
                    'udland': 0.20,
                    'samfund': 0.15,
                    'kultur': 0.15
                },
                'fact_checking': 0.85,
                'transparency': 0.84,
                'category': 'Landsdækkende',
                'description': 'Liberal-konservativ avis med fokus på politik og erhverv'
            },
            
            # Public Service
            'DR': {
                'political_bias': -0.1,
                'reliability_score': 0.90,
                'source_diversity': 0.88,
                'topic_coverage': {
                    'politik': 0.20,
                    'samfund': 0.20,
                    'kultur': 0.20,
                    'udland': 0.20,
                    'regional': 0.20
                },
                'fact_checking': 0.91,
                'transparency': 0.89,
                'category': 'Public Service',
                'description': 'Public service medie med bred dækning af alle samfundsområder'
            },
            'TV2': {
                'political_bias': 0.0,
                'reliability_score': 0.88,
                'source_diversity': 0.86,
                'topic_coverage': {
                    'politik': 0.25,
                    'samfund': 0.25,
                    'regional': 0.20,
                    'sport': 0.15,
                    'underholdning': 0.15
                },
                'fact_checking': 0.87,
                'transparency': 0.86,
                'category': 'Public Service',
                'description': 'Kommercielt public service medie med fokus på nyheder og underholdning'
            },
            
            # Tabloid
            'BT': {
                'political_bias': 0.2,
                'reliability_score': 0.75,
                'source_diversity': 0.72,
                'topic_coverage': {
                    'underholdning': 0.30,
                    'sport': 0.25,
                    'krimi': 0.20,
                    'samfund': 0.15,
                    'politik': 0.10
                },
                'fact_checking': 0.76,
                'transparency': 0.74,
                'category': 'Tabloid',
                'description': 'Tabloidavis med fokus på underholdning, sport og breaking news'
            },
            'Ekstra Bladet': {
                'political_bias': -0.2,
                'reliability_score': 0.72,
                'source_diversity': 0.70,
                'topic_coverage': {
                    'underholdning': 0.35,
                    'krimi': 0.25,
                    'sport': 0.20,
                    'politik': 0.10,
                    'samfund': 0.10
                },
                'fact_checking': 0.73,
                'transparency': 0.71,
                'category': 'Tabloid',
                'description': 'Tabloidavis kendt for undersøgende journalistik og underholdning'
            },
            
            # Niche
            'Altinget': {
                'political_bias': 0.0,
                'reliability_score': 0.92,
                'source_diversity': 0.90,
                'topic_coverage': {
                    'politik': 0.60,
                    'samfund': 0.20,
                    'eu': 0.10,
                    'økonomi': 0.05,
                    'miljø': 0.05
                },
                'fact_checking': 0.93,
                'transparency': 0.91,
                'category': 'Niche',
                'description': 'Politisk nichemedie med fokus på Christiansborg og EU'
            },
            'Zetland': {
                'political_bias': -0.3,
                'reliability_score': 0.89,
                'source_diversity': 0.87,
                'topic_coverage': {
                    'samfund': 0.35,
                    'kultur': 0.25,
                    'klima': 0.20,
                    'teknologi': 0.10,
                    'videnskab': 0.10
                },
                'fact_checking': 0.90,
                'transparency': 0.92,
                'category': 'Niche',
                'description': 'Digitalt medie med fokus på dybdegående journalistik'
            },
            
            # Erhverv
            'Børsen': {
                'political_bias': 0.4,
                'reliability_score': 0.87,
                'source_diversity': 0.85,
                'topic_coverage': {
                    'erhverv': 0.40,
                    'økonomi': 0.30,
                    'finans': 0.15,
                    'politik': 0.10,
                    'teknologi': 0.05
                },
                'fact_checking': 0.88,
                'transparency': 0.86,
                'category': 'Erhverv',
                'description': 'Erhvervsavis med fokus på økonomi, finans og erhvervsliv'
            },
            'Finans': {
                'political_bias': 0.3,
                'reliability_score': 0.86,
                'source_diversity': 0.84,
                'topic_coverage': {
                    'erhverv': 0.35,
                    'økonomi': 0.35,
                    'finans': 0.15,
                    'politik': 0.10,
                    'teknologi': 0.05
                },
                'fact_checking': 0.87,
                'transparency': 0.85,
                'category': 'Erhverv',
                'description': 'Digital erhvervsavis med fokus på erhverv og økonomi'
            },
            'MediaWatch': {
                'political_bias': 0.0,
                'reliability_score': 0.88,
                'source_diversity': 0.86,
                'topic_coverage': {
                    'medier': 0.60,
                    'tech': 0.15,
                    'reklame': 0.10,
                    'erhverv': 0.10,
                    'politik': 0.05
                },
                'fact_checking': 0.89,
                'transparency': 0.87,
                'category': 'Erhverv',
                'description': 'Branchemedie med fokus på medie- og reklamebranchen'
            },
            
            # Regionale medier
            'TV2 Nord': {
                'political_bias': 0.0,
                'reliability_score': 0.85,
                'source_diversity': 0.82,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.84,
                'transparency': 0.85,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Nordjylland'
            },
            'TV2 Øst': {
                'political_bias': 0.1,
                'reliability_score': 0.84,
                'source_diversity': 0.81,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.83,
                'transparency': 0.84,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Sjælland og øerne'
            },
            'TV2 Fyn': {
                'political_bias': -0.1,
                'reliability_score': 0.85,
                'source_diversity': 0.83,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.84,
                'transparency': 0.85,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Fyn og øerne'
            },
            'TV2 Lorry': {
                'political_bias': -0.1,
                'reliability_score': 0.86,
                'source_diversity': 0.84,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.25,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.85,
                'transparency': 0.86,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker hovedstadsområdet'
            },
            'TV MIDTVEST': {
                'political_bias': 0.1,
                'reliability_score': 0.84,
                'source_diversity': 0.82,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.83,
                'transparency': 0.84,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Midt- og Vestjylland'
            },
            'TV SYD': {
                'political_bias': 0.1,
                'reliability_score': 0.85,
                'source_diversity': 0.82,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.84,
                'transparency': 0.85,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Syd- og Sønderjylland'
            },
            'TV2 Østjylland': {
                'political_bias': 0.0,
                'reliability_score': 0.85,
                'source_diversity': 0.83,
                'topic_coverage': {
                    'lokalt': 0.45,
                    'samfund': 0.20,
                    'kultur': 0.15,
                    'erhverv': 0.10,
                    'sport': 0.10
                },
                'fact_checking': 0.84,
                'transparency': 0.85,
                'category': 'Regional',
                'description': 'Regional TV2-kanal der dækker Østjylland'
            },
            'Nordjyske': {
                'political_bias': 0.2,
                'reliability_score': 0.83,
                'source_diversity': 0.80,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.20,
                    'erhverv': 0.15,
                    'kultur': 0.15,
                    'sport': 0.10
                },
                'fact_checking': 0.82,
                'transparency': 0.83,
                'category': 'Regional',
                'description': 'Regional avis der dækker Nordjylland'
            },
            'JydskeVestkysten': {
                'political_bias': 0.2,
                'reliability_score': 0.84,
                'source_diversity': 0.81,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.20,
                    'erhverv': 0.15,
                    'kultur': 0.15,
                    'sport': 0.10
                },
                'fact_checking': 0.83,
                'transparency': 0.84,
                'category': 'Regional',
                'description': 'Regional avis der dækker Syd- og Sønderjylland'
            },
            'Fyens Stiftstidende': {
                'political_bias': 0.1,
                'reliability_score': 0.84,
                'source_diversity': 0.81,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.20,
                    'erhverv': 0.15,
                    'kultur': 0.15,
                    'sport': 0.10
                },
                'fact_checking': 0.83,
                'transparency': 0.84,
                'category': 'Regional',
                'description': 'Regional avis der dækker Fyn og øerne'
            },
            'Århus Stiftstidende': {
                'political_bias': 0.1,
                'reliability_score': 0.84,
                'source_diversity': 0.81,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.20,
                    'erhverv': 0.15,
                    'kultur': 0.15,
                    'sport': 0.10
                },
                'fact_checking': 0.83,
                'transparency': 0.84,
                'category': 'Regional',
                'description': 'Regional avis der dækker Østjylland'
            },
            'Sjællandske Medier': {
                'political_bias': 0.1,
                'reliability_score': 0.83,
                'source_diversity': 0.80,
                'topic_coverage': {
                    'lokalt': 0.40,
                    'samfund': 0.20,
                    'erhverv': 0.15,
                    'kultur': 0.15,
                    'sport': 0.10
                },
                'fact_checking': 0.82,
                'transparency': 0.83,
                'category': 'Regional',
                'description': 'Regional mediegruppe der dækker Sjælland'
            }
        },
        'categories': MEDIA_CATEGORIES
    })

if __name__ == '__main__':
    app.run(debug=True)
