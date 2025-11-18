from fastapi import FastAPI
from api.database
from api.models import Article

app=FastAPI()

@app.get("/articles/")
def list_articles():
    db= SessionLocal()
    articles = db.query(Article).order_by(Article.id.desc()).all()
    db.close()
    return articles

