import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict
import logging
from datetime import datetime
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import asyncio
import aiohttp
from urllib.parse import urljoin
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MediaScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Udvidet liste af danske nyhedskilder med deres specifik konfiguration
        self.news_sources = {
            'dr': {
                'url': 'https://www.dr.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': False
            },
            'tv2': {
                'url': 'https://nyheder.tv2.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article__body',
                'requires_js': True
            },
            'politiken': {
                'url': 'https://politiken.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'berlingske': {
                'url': 'https://www.berlingske.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'information': {
                'url': 'https://www.information.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': False
            },
            'jyllandsposten': {
                'url': 'https://jyllands-posten.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'ekstrabladet': {
                'url': 'https://ekstrabladet.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'bt': {
                'url': 'https://www.bt.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'kristeligt-dagblad': {
                'url': 'https://www.kristeligt-dagblad.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-content',
                'requires_js': True
            },
            'borsen': {
                'url': 'https://borsen.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'altinget': {
                'url': 'https://www.altinget.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            },
            'finans': {
                'url': 'https://finans.dk',
                'article_selector': 'article',
                'title_selector': 'h1',
                'content_selector': '.article-body',
                'requires_js': True
            }
        }
        
        # Setup Selenium
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_options)

    async def fetch_articles_async(self, source: str, limit: int = 10) -> List[Dict]:
        """
        Asynkron artikel-hentning med støtte for JavaScript-renderede sider
        """
        try:
            articles = []
            source_config = self.news_sources.get(source)
            
            if not source_config:
                logger.error(f"Ukendt nyhedskilde: {source}")
                return articles

            if source_config['requires_js']:
                articles = await self._fetch_with_selenium(source_config, limit)
            else:
                articles = await self._fetch_with_requests(source_config, limit)

            return articles

        except Exception as e:
            logger.error(f"Fejl ved hentning af artikler fra {source}: {str(e)}")
            return []

    async def _fetch_with_selenium(self, source_config: Dict, limit: int) -> List[Dict]:
        """
        Henter artikler fra JavaScript-renderede sider
        """
        articles = []
        self.driver.get(source_config['url'])
        
        # Vent på at artikler bliver loaded
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, source_config['article_selector']))
        )
        
        # Find alle artikel-links
        article_elements = self.driver.find_elements(By.CSS_SELECTOR, source_config['article_selector'])
        article_links = []
        
        for element in article_elements[:limit]:
            try:
                link = element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                article_links.append(link)
            except:
                continue
        
        # Hent hver artikel
        for link in article_links:
            try:
                article = Article(link, language='da')
                article.download()
                article.parse()
                
                articles.append({
                    'title': article.title,
                    'content': article.text,
                    'url': link,
                    'source': source_config['url'],
                    'timestamp': article.publish_date.isoformat() if article.publish_date else datetime.now().isoformat(),
                    'authors': article.authors,
                    'keywords': article.keywords
                })
            except Exception as e:
                logger.error(f"Fejl ved parsing af artikel {link}: {str(e)}")
                continue
                
        return articles

    async def _fetch_with_requests(self, source_config: Dict, limit: int) -> List[Dict]:
        """
        Henter artikler fra standard HTML sider
        """
        articles = []
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(source_config['url']) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    for article in soup.select(source_config['article_selector'])[:limit]:
                        try:
                            link = article.find('a')['href']
                            if not link.startswith('http'):
                                link = urljoin(source_config['url'], link)
                                
                            async with session.get(link) as article_response:
                                if article_response.status == 200:
                                    article_html = await article_response.text()
                                    article_soup = BeautifulSoup(article_html, 'html.parser')
                                    
                                    title = article_soup.select_one(source_config['title_selector'])
                                    content = article_soup.select_one(source_config['content_selector'])
                                    
                                    if title and content:
                                        articles.append({
                                            'title': title.text.strip(),
                                            'content': content.text.strip(),
                                            'url': link,
                                            'source': source_config['url'],
                                            'timestamp': datetime.now().isoformat()
                                        })
                        except Exception as e:
                            logger.error(f"Fejl ved parsing af artikel: {str(e)}")
                            continue
                            
        return articles

    def clean_text(self, text: str) -> str:
        """
        Avanceret tekstrensning
        """
        # Fjern HTML tags
        soup = BeautifulSoup(text, "html.parser")
        text = soup.get_text()
        
        # Fjern ekstra whitespace
        text = " ".join(text.split())
        
        # Fjern specialtegn
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        
        return text.strip()

    def save_to_json(self, articles: List[Dict], filename: str):
        """
        Gem artikler i JSON format med metadata
        """
        try:
            output = {
                'metadata': {
                    'timestamp': datetime.now().isoformat(),
                    'total_articles': len(articles),
                    'sources': list(set(article['source'] for article in articles))
                },
                'articles': articles
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(output, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Artikler gemt i {filename}")
        except Exception as e:
            logger.error(f"Fejl ved gemning af artikler: {str(e)}")

    def __del__(self):
        """
        Luk Selenium driver når objektet bliver destroyed
        """
        if hasattr(self, 'driver'):
            self.driver.quit()

if __name__ == "__main__":
    async def main():
        scraper = MediaScraper()
        all_articles = []
        
        # Test scraping fra alle kilder
        for source in scraper.news_sources.keys():
            articles = await scraper.fetch_articles_async(source, limit=5)
            all_articles.extend(articles)
            print(f"Hentet {len(articles)} artikler fra {source}")
            
        # Gem resultater
        scraper.save_to_json(all_articles, 'articles.json')
    
    asyncio.run(main())
