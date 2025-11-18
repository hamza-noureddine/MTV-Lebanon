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

articles = data

for article in articles:
  
    article_id = article.get("articleid")
    title = article.get("title")
    media_url = article.get("MediaUrl")
    category = article.get("articletype")
    url_path = article.get("Url")  # already a full path

    full_url = f"https://www.mtv.com.lb{url_path}"

    print("ID:", article_id)
    print("Category:", category)
    print("URL:", full_url)
    print("Title:", title)
    print("Image:", media_url)
    print("-" * 60)