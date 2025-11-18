import requests
from bs4 import BeautifulSoup
from api.database import SessionLocal
from api.models import Article

BASE_URL = "https://www.mtv.com.lb"
API_URL = "https://www.mtv.com.lb/en/api/articles"

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


def fetch_article_list(start=0, batch=30):
    """Fetch a batch of MTV articles."""
    url = f"{API_URL}?start={start}&end={start+batch}&type="
    response = requests.get(url, headers=HEADERS)
    try:
        data = response.json()
        return data
    except:
        return []



# Parse individual article page

def parse_article_page(url):
    html = requests.get(url, headers=HEADERS).text
    soup = BeautifulSoup(html, "html.parser")

    title_el = soup.select_one(".section-header-text")
    date_el = soup.select_one(".articles-header-date .black")
    time_el = soup.select_one(".articles-header-date .red")
    text_el = soup.select_one("#mainContent")

    result = {
        "title": title_el.get_text(strip=True) if title_el else "",
        "date": date_el.get_text(strip=True) if date_el else "",
        "time": time_el.get_text(strip=True) if time_el else "",
        "text": text_el.get_text("\n", strip=True) if text_el else "",
        "url": url,
        "category": url.split("/")[5] if len(url.split("/")) > 5 else "",
        "is_video": False,
        "image": None,
        "video_poster": None,
        "video_url": None,
    }

    # Check if video exists
    video = soup.select_one("div.video-player-container")
    if video:
        result["is_video"] = True
        result["video_poster"] = video.get("poster")
        src = video.find("source", {"type": "application/x-mpegURL"})
        if src:
            result["video_url"] = src.get("src")

    else:
        # Extract normal image
        img = soup.select_one(".articles-header-image img")
        if img:
            result["image"] = img.get("src")

    return result



def run_scraper(pages=5, batch_size=30):
    
    "Run the MTV Lebanon scraper to fetch and store articles in the database"
    

    db = SessionLocal()
    scraped_count = 0

    for page in range(pages):
        start = page * batch_size
        print(f"\ntestttt Fetching list batch {page+1} (start={start})...")

        items = fetch_article_list(start=start, batch=batch_size)
        if not items:
            print("No more articles found. Stopping.")
            break

        for item in items:
            article_id = item.get("articleid")
            if not article_id:
                continue

            # Duplicate check by article_id
            exists = db.query(Article).filter_by(article_id=article_id).first()
            if exists:
                print(f"⏭ Skipping (already in DB): {article_id}")
                continue

            # Scrape article
            url = BASE_URL + item["Url"]
            print(f"📝 Scraping NEW article {article_id} → {url}")

            parsed = parse_article_page(url)
            parsed["article_id"] = article_id

            # Save to DB
            article = Article(**parsed)
            db.add(article)
            db.commit()
            scraped_count += 1

    db.close()
    print(f"\nDONEee scraped {scraped_count} new articles.")


if __name__ == "__main__":
    run_scraper(pages=3)

