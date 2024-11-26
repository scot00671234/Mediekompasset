from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Define media outlets with their characteristics
media_outlets = {
    'dr': {
        'name': 'DR',
        'bias': -0.2,
        'reliability': 0.95,
        'metrics': {
            'political_bias': -0.2,
            'factuality': 0.95,
            'source_diversity': 0.88,
            'topic_balance': 0.85,
            'language_complexity': 0.7
        },
        'top_topics': ['Politik', 'Kultur', 'Samfund', 'Økonomi']
    },
    'tv2': {
        'name': 'TV2',
        'bias': 0.1,
        'reliability': 0.92,
        'metrics': {
            'political_bias': 0.1,
            'factuality': 0.92,
            'source_diversity': 0.82,
            'topic_balance': 0.80,
            'language_complexity': 0.65
        },
        'top_topics': ['Nyheder', 'Sport', 'Politik', 'Underholdning']
    }
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Mediekompasset - Din Guide til Danske Medier",
            "media_outlets": media_outlets
        }
    )

@app.get("/analyze/{media_id}", response_class=HTMLResponse)
async def analyze_media(request: Request, media_id: str):
    if media_id not in media_outlets:
        raise HTTPException(status_code=404, detail="Medie ikke fundet")
    
    return templates.TemplateResponse(
        "analysis.html",
        {
            "request": request,
            "title": f"{media_outlets[media_id]['name']} Analyse - Mediekompasset",
            "media": media_outlets[media_id],
            "media_id": media_id
        }
    )

@app.get("/methodology", response_class=HTMLResponse)
async def methodology(request: Request):
    return templates.TemplateResponse(
        "methodology.html",
        {
            "request": request,
            "title": "Metodologi - Mediekompasset"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
