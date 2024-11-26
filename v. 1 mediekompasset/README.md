# Dansk Medie Bias Analyse

En webapplikation til analyse af politisk bias i danske massemedier.

## Installation

1. Opret et virtuelt miljø:
```bash
python -m venv venv
source venv/bin/activate  # På Windows: venv\Scripts\activate
```

2. Installer afhængigheder:
```bash
pip install -r requirements.txt
```

3. Download dansk sprogmodel til spaCy:
```bash
python -m spacy download da_core_news_sm
```

4. Start applikationen:
```bash
uvicorn main:app --reload
```

## Funktioner

- Tekstanalyse af nyhedsartikler
- Sentiment analyse
- Kildesporing
- Ordfrekvensanalyse
- Visualisering af politisk bias

## Metodologi

Applikationen bruger følgende metoder til at analysere mediebias:

1. NLP-baseret tekstanalyse
2. Sentiment analyse af politiske emner
3. Kildesporing og ekspertanalyse
4. Ordfrekvensanalyse
5. Emnefordelingsanalyse

## Database Setup

1. Opret en PostgreSQL database
2. Opdater .env filen med dine database credentials
