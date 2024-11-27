# Mediekompasset

En web-applikation til analyse af danske massemediers dækning og bias.

## Funktioner

- Automatisk indsamling af nyheder fra større danske medier
- Analyse af politisk orientering
- Kildekritisk analyse
- Emnebehandling
- Pålidelighedsanalyse
- Visualisering af resultater

## Installation

1. Installer Python 3.9 eller nyere
2. Installer afhængigheder:
```bash
pip install -r requirements.txt
```
3. Installer Node.js og npm
4. Installer frontend afhængigheder:
```bash
cd frontend
npm install
```

## Kørsel af applikationen

1. Start backend server:
```bash
python app.py
```

2. Start frontend development server:
```bash
cd frontend
npm start
```

## Teknologier

- Backend: Python, Flask, Transformers (NLP)
- Frontend: React, Material-UI
- Data Analysis: Pandas, Scikit-learn
- Web Scraping: Newspaper3k, BeautifulSoup4
