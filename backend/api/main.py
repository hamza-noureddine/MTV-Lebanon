from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from api.database import SessionLocal, engine
from api.models import Article, Base
from scraper import run_scraper

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# CORS CONFIG
origins = [
    "https://mtv-lebanon.vercel.app",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "API Running"}



def parse_datetime(article):
    """Combine date + time → real datetime object."""
    dt_str = f"{article.date} {article.time}".strip()

    try:
        return datetime.strptime(dt_str, "%d %b %Y %I:%M %p")
    except:
        return datetime.min 


@app.get("/articles")
def list_articles():
    db = SessionLocal()
    articles = db.query(Article).all()
    db.close()

    # Sort newest → oldest
    sorted_articles = sorted(articles, key=parse_datetime, reverse=True)

    return sorted_articles


@app.post("/scrape")
def trigger_scrape():
    run_scraper()
    return {"status": "scraped"}
