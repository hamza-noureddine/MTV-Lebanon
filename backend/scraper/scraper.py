from bs4 import BeautifulSoup
import requests
from api.database import SessionLocal
from api.models import Article


def fetch_article_list(limit=50):
   url = f"https://www.mtv.com.lb/en/api/articles?start=0&end={limit}&type="
   headers = {'sec-ch-ua-platform': '"Windows"',
  'Referer': 'https://www.mtv.com.lb/en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
  'sec-ch-ua-mobile': '?0' }
   
   return requests.get(url, headers=headers).json()
 
 
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
  video = soup.select_one("div.video-player-container")
  if video:
      result["is_video"] = True
      result["video_poster"] = video.get("poster")
      source = video.find("source", {"type": "application/x-mpegURL"})
      if source:
          result["video_url"] = source.get("src")
          
  else:
    img = soup.select_one(".articles-header-image img")
    if img:
        result["image"] = img.get("src")

    return result


def run_scraper():
  db = SessionLocal()
  items = fetch_article_list()
  for item in items:
      url = "https://www.mtv.com.lb" + item["Url"]
      exists = db.query(Article).filter_by(url=url).first()
      if exists:
          continue
        
      parsed = parse_article_page(url)
      article = Article(**parsed)
      db.add(article)
      db.commit()
  db.close()
  
if __name__ == "__main__":
    run_scraper()
      