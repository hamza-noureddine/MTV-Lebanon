from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.database import SessionLocal, engine
from api.models import Article, Base
from scraper import run_scraper

app = FastAPI()

# Create DB tables
Base.metadata.create_all(bind=engine)

# CORS settings
origins = [
    "https://mtv-lebanon.vercel.app",
    "https://mtv-lebanon-fmh54tpoa-hamzas-projects-da37ea56.vercel.app",
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

@app.get("/articles")
def list_articles():
    db = SessionLocal()
    articles = db.query(Article).order_by(Article.id.desc()).all()
    db.close()
    return articles


@app.post("/scrape")
def trigger_scrape():
    new_count = run_scraper()
    
    if new_count == 0:
        return {"status": "ok", "message": "No new articles found."}

    return {"status": "ok", "message": f"Fetched {new_count} new articles."}

