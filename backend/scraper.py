import requests
from bs4 import BeautifulSoup
from api.database import SessionLocal, engine
from api.models import Article, Base


API_LIST_URL = "https://www.mtv.com.lb/en/api/articles?start=0&end=50&type="

HEADERS = {
    'accept': 'application/json, text/plain, */*',
  'accept-language': 'en-US,en;q=0.9,de;q=0.8',
  'if-modified-since': 'Tue, 18 Nov 2025 15:53:18 GMT',
  'priority': 'u=1, i',
  'referer': 'https://www.mtv.com.lb/en/',
  'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
  'Cookie': '_fbp=fb.2.1763469085468.430836885533764322; _ga=GA1.1.221080451.1763469087; _mbj=mbj:a42afb14-87a6-4a27-b3bf-4be490521860; __gads=ID=71ad6fdfa1ea52fa:T=1763469026:RT=1763499012:S=ALNI_MbEVp45PjOslP4upH3SHXF-8NFKaA; __eoi=ID=ff87665738f2b9a6:T=1763469026:RT=1763499012:S=AA-AfjY4vpSve1NAqfPRILU7k0rn; _ga_JKWJKTW39H=GS2.1.s1763498996$o3$g1$t1763499252$j59$l0$h549407909; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%2241494afa-7acb-4526-9e24-d5dc6a27b4f8%5C%22%2C%5B1763469080%2C307000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol9D4OUvcJzd_jP3oTzKxdlzWlrmPmwPg3VsoBG8oNkVCjXKWNIp3slUYJMMW-2egL0jr47Wgj46-s-mJSAXwyDLMPyOERx8pYBv8BCli7f5QzVMM7p5av0UuWK30NTq24nsFzI21jx-qu0SVXRIVGfMNFhkeg%3D%3D%22%5D%5D'
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
        print(f"Saved: {parsed['title']}")

    print(f"\n Done — {saved} new articles added.")
    db.close()



if __name__ == "__main__":
    run_scraper()
