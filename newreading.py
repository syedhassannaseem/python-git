import requests
import json
want = input("What news do u want to Read: ")
url=requests.get(f"https://newsapi.org/v2/everything?q={want}&from=2025-03-13&sortBy=publishedAt&apiKey=9b35fa69b5884d9292b8e110c783b72e")
print(url.status_code)
new=json.loads(url.text)
for article in new["articles"]:
  print(article["title"])
  print(article["description"])
