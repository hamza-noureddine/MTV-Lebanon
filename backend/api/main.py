from fastapi import FastAPI
from api.database import SessionLocal, engine
from api.models import Article, Base
from scraper import run_scraper

app = FastAPI()

# create tables if not exist
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"status": "API Running"}

@app.get("/articles")
def list_articles():
    db = SessionLocal()
    articles = db.query(Article).order_by(Article.id.desc()).all()
    db.close()
    return articles

@app.get("/scrape")
def scrape_now():
    run_scraper()
    return {"status": "scraped"}
