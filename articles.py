import requests


end=30
url = f"https://www.mtv.com.lb/en/api/articles?start=0&end={end}&type="


headers = {
  'sec-ch-ua-platform': '"Windows"',
  'Referer': 'https://www.mtv.com.lb/en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
  'sec-ch-ua-mobile': '?0'
}

response = requests.request("GET", url, headers=headers)


data = response.json()

articles = data.get("articles", [])

print(f"Retrieved {len(articles)} articles:")


for article in articles:
    article_id = article.get("id")
    category = article.get("type")
    subcategory = article.get("category") or "Local"
    
    # iterate through each article's url
    article_url = f"https://www.mtv.com.lb/en/news/{subcategory}/{article_id}"
    
    print("ID:", article_id)
    print("URL:", article_url)
    
    
