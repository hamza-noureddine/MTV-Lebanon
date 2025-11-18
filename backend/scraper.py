import requests
from bs4 import BeautifulSoup
from api.database import SessionLocal, engine
from api.models import Article, Base


API_LIST_URL = "https://www.mtv.com.lb/en/api/articles?start=0&end=50&type="

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/plain, */*"
}

# Ensure database tables exist
Base.metadata.create_all(bind=engine)



def fetch_article_list():
    print(" Fetching article list...")
    res = requests.get(API_LIST_URL, headers=HEADERS)
    res.raise_for_status()
    return res.json()



def parse_article(url):
    print(f"Parsing article: {url}")
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    def safe(sel):
        el = soup.select_one(sel)
        return el.get_text(strip=True) if el else None

  
    def safe_img(sel):
        el = soup.select_one(sel)
        return el.get("src") if el else None

    title   = safe(".section-header-text")
    date    = safe(".articles-header-date .black")
    time    = safe(".articles-header-date .red")
    text    = safe("#mainContent")
    image   = safe_img(".articles-header-image img")

  
    category = None
    meta_url = soup.find("meta", {"property": "og:url"})
    if meta_url:
        try:
            category = meta_url["content"].split("/")[5]
        except:
            category = None

   
    video_block = soup.select_one("div.video-player-container")
    is_video = video_block is not None
    video_poster = video_block.get("poster") if is_video else None

    video_url = None
    if is_video:
        source = video_block.find("source", {"type": "application/x-mpegURL"})
        if source:
            video_url = source.get("src")

    return {
        "title": title,
        "date": date,
        "time": time,
        "text": text,
        "category": category,
        "url": url,
        "image": image,
        "is_video": is_video,
        "video_poster": video_poster,
        "video_url": video_url
    }



def run_scraper():
    db = SessionLocal()
    items = fetch_article_list()

    saved = 0

    for item in items:
        url = "https://www.mtv.com.lb" + item["Url"]

        # Skip if already in DB
        if db.query(Article).filter_by(url=url).first():
            print(f" Already exists: {url}")
            continue

        parsed = parse_article(url)

        
        if not parsed["title"]:
            print(f" Skipping (no title): {url}")
            continue

        article = Article(**parsed)
        db.add(article)
        db.commit()
        saved += 1
        print(f"✅ Saved: {parsed['title']}")

    print(f"\n Done — {saved} new articles added.")
    db.close()



if __name__ == "__main__":
    run_scraper()
