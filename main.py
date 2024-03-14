import lxml
import json
import parsel
import requests

url = 'https://books.toscrape.com/'
user_id = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}
response = requests.get(url=url, headers=user_id)

with open('quotes.html.html', 'w', encoding='utf-8') as file:
    file.write(response.text)

with open('quotes.html', 'r') as file:
    html = file.read()




#print(parse(response))
print(json.dumps(parse(response), indent=2, ensure_ascii=False))
