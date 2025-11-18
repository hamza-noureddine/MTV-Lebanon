import requests

url = "https://www.mtv.com.lb/en/api/reels"

payload = {}
headers = {
  'sec-ch-ua-platform': '"Windows"',
  'Referer': 'https://www.mtv.com.lb/en',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
  'sec-ch-ua-mobile': '?0'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
