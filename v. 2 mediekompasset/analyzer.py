import spacy
import pandas as pd
from typing import Dict, List, Tuple
from collections import Counter
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BiasAnalyzer:
    def __init__(self):
        self.nlp = spacy.load('da_core_news_sm')
        self.tokenizer = AutoTokenizer.from_pretrained('Maltehb/danish-bert-botxo')
        self.model = AutoModelForSequenceClassification.from_pretrained('Maltehb/danish-bert-botxo')
        
        # Udvidet politiske nøgleord
        self.political_keywords = {
            'venstre': {
                'solidaritet': 1.0,
                'velfærd': 0.8,
                'lighed': 0.9,
                'fællesskab': 0.7,
                'offentlig': 0.6,
                'fagforening': 0.8,
                'arbejderrettigheder': 0.9,
                'klimahandling': 0.7,
                'bæredygtighed': 0.6,
                'mangfoldighed': 0.7
            },
            'højre': {
                'frihed': 1.0,
                'marked': 0.8,
                'skattelettelser': 0.9,
                'privat': 0.7,
                'individ': 0.6,
                'erhvervsliv': 0.8,
                'konkurrence': 0.7,
                'vækst': 0.6,
                'innovation': 0.6,
                'iværksætteri': 0.7
            }
        }
        
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.kmeans = KMeans(n_clusters=3)
        self.pca = PCA(n_components=2)

    def analyze_text(self, text: str) -> Dict:
        """
        Avanceret tekstanalyse med både regelbaseret og ML-baseret tilgang
        """
        doc = self.nlp(text.lower())
        
        # Basis analyse
        word_counts = Counter(token.text for token in doc if not token.is_stop)
        
        # BERT-baseret analyse
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        bert_sentiment = torch.nn.functional.softmax(outputs.logits, dim=1)
        
        # Regelbaseret analyse
        left_score = sum(word_counts[word] * weight 
                        for word, weight in self.political_keywords['venstre'].items() 
                        if word in word_counts)
        
        right_score = sum(word_counts[word] * weight 
                         for word, weight in self.political_keywords['højre'].items() 
                         if word in word_counts)
        
        # Kombiner scores
        total_score = left_score + right_score
        if total_score > 0:
            rule_based_score = (right_score - left_score) / total_score
        else:
            rule_based_score = 0
            
        # Kombiner regelbaseret og ML-baseret score
        final_score = (rule_based_score + bert_sentiment[0][1].item()) / 2
            
        return {
            'bias_score': final_score,
            'confidence': min(total_score / 10, 1.0),
            'word_frequencies': dict(word_counts.most_common(10)),
            'bert_sentiment': bert_sentiment[0][1].item(),
            'rule_based_score': rule_based_score
        }

    def create_visualizations(self, articles: List[Dict], output_dir: str):
        """
        Opret forskellige visualiseringer af data
        """
        # Word cloud
        text = ' '.join([article['content'] for article in articles])
        wordcloud = WordCloud(width=800, height=400, 
                            background_color='white',
                            colormap='viridis').generate(text)
        
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(f'{output_dir}/wordcloud.png')
        
        # Bias distribution
        bias_scores = [self.analyze_text(article['content'])['bias_score'] 
                      for article in articles]
        
        plt.figure(figsize=(10, 5))
        sns.histplot(bias_scores, bins=20)
        plt.title('Distribution af Politisk Bias')
        plt.xlabel('Bias Score')
        plt.ylabel('Antal Artikler')
        plt.savefig(f'{output_dir}/bias_distribution.png')
        
        # Topic clustering
        texts = [article['content'] for article in articles]
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        clusters = self.kmeans.fit_predict(tfidf_matrix.toarray())
        
        # Reducer dimensioner for visualisering
        reduced_data = self.pca.fit_transform(tfidf_matrix.toarray())
        
        plt.figure(figsize=(10, 5))
        scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], 
                            c=clusters, cmap='viridis')
        plt.title('Emne Clustering')
        plt.colorbar(scatter)
        plt.savefig(f'{output_dir}/topic_clusters.png')

    def analyze_sources(self, articles: List[Dict]) -> Dict:
        """
        Analyserer flere artikler fra forskellige kilder med avanceret statistik
        """
        results = {}
        
        for article in articles:
            source = article['source']
            if source not in results:
                results[source] = []
                
            analysis = self.analyze_text(article['content'])
            results[source].append(analysis)
        
        # Aggregér resultater med mere detaljeret statistik
        aggregated_results = {}
        for source, analyses in results.items():
            bias_scores = [a['bias_score'] for a in analyses]
            confidence_scores = [a['confidence'] for a in analyses]
            bert_scores = [a['bert_sentiment'] for a in analyses]
            
            aggregated_results[source] = {
                'average_bias': np.mean(bias_scores),
                'median_bias': np.median(bias_scores),
                'std_bias': np.std(bias_scores),
                'confidence': np.mean(confidence_scores),
                'bert_sentiment_avg': np.mean(bert_scores),
                'sample_size': len(analyses),
                'bias_percentiles': {
                    '25': np.percentile(bias_scores, 25),
                    '50': np.percentile(bias_scores, 50),
                    '75': np.percentile(bias_scores, 75)
                }
            }
            
        return aggregated_results

    def get_source_citations(self, text: str) -> List[Tuple[str, str]]:
        """
        Identificerer og kategoriserer kilder citeret i teksten
        """
        doc = self.nlp(text)
        citations = []
        
        # Simpel implementation - kan udvides med mere avanceret NER
        for ent in doc.ents:
            if ent.label_ in ['PER', 'ORG']:
                citations.append((ent.text, ent.label_))
                
        return citations

    def export_analysis(self, results: Dict, filename: str):
        """
        Eksporterer analyseresultater til CSV
        """
        df = pd.DataFrame.from_dict(results, orient='index')
        df.to_csv(filename)
        logger.info(f"Analyse eksporteret til {filename}")

if __name__ == "__main__":
    analyzer = BiasAnalyzer()
    # Test analyse
    test_text = """
    Regeringen foreslår nye skattelettelser for at styrke det private erhvervsliv,
    mens oppositionen argumenterer for mere velfærd og social solidaritet.
    """
    result = analyzer.analyze_text(test_text)
    print(f"Test analyse resultat: {result}")
