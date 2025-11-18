from fastapi import FastAPI
from api.database import SessionLocal, engine
from api.models import Article, Base
from scraper import run_scraper
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# create tables if not exist
Base.metadata.create_all(bind=engine)

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

@app.get("/articles")
def list_articles():
    db = SessionLocal()
    articles = db.query(Article).order_by(Article.id.desc()).all()
    db.close()
    return articles

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

@app.get("/scrape")
def scrape_now():
    run_scraper()
    return {"status": "scraped"}




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


@app.post("/scrape")
def trigger_scrape():
    run_scraper()
    return {"status": "scraped"}

