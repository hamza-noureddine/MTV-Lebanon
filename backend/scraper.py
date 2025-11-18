from bs4 import BeautifulSoup
import requests
from api.database import SessionLocal
from api.models import Article

API_LIST_URL = "https://www.mtv.com.lb/en/api/articles?start=0&end=50&type="


def fetch_article_list():
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
    return requests.get(API_LIST_URL, headers=HEADERS).json()


def parse_article_page(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")

    result = {
        "title": soup.select_one(".section-header-text").get_text(strip=True),
        "date": soup.select_one(".articles-header-date .black").get_text(strip=True),
        "time": soup.select_one(".articles-header-date .red").get_text(strip=True),
        "text": soup.select_one("#mainContent").get_text("\n", strip=True),
        "category": soup.find("meta", {"property": "og:url"})["content"].split("/")[5],
        "url": url,
        "is_video": False,
        "image": None,
        "video_poster": None,
        "video_url": None
    }

    # VIDEO HANDLING
    video = soup.select_one("div.video-player-container")
    if video:
        result["is_video"] = True
        result["video_poster"] = video.get("poster")
        src = video.find("source", {"type": "application/x-mpegURL"})
        if src:
            result["video_url"] = src.get("src")
    else:
        img = soup.select_one(".articles-header-image img")
        if img:
            result["image"] = img.get("src")

    return result


def run_scraper():
    """
    Returns:
        new_count: number of new articles inserted
    """
    db = SessionLocal()

    items = list(reversed(fetch_article_list()))


    new_articles = 0

    for item in items:
        full_url = "https://www.mtv.com.lb" + item["Url"]

        # Check if already exists
        exists = db.query(Article).filter_by(url=full_url).first()
        if exists:
            continue

        print("🆕 New article found:", full_url)

        parsed = parse_article_page(full_url)
        article = Article(**parsed)
        db.add(article)
        db.commit()

        new_articles += 1

    db.close()
    return new_articles
