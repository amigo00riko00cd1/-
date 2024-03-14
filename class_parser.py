import lxml
import json
import parsel
import requests


class Parser_git:

    def __init__(self, url, name='file_pivo'):
        self.url = url
        self.user_id = self.get_user_id()
        self.response = self.get_response()
        self.save_file(self.response, name)
        self.f = 0

    def get_user_id(self) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        }

    def get_response(self):
        return requests.get(url=self.url, headers=self.user_id)

    def save_file(self, response, name):
        with open(f'{name}.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

    def read_file(self, name):
        with open(f'{name}.html', 'r') as file:
            html = file.read()
            return html

    def parse(self):
        data = []
        while True:
            selector = parsel.Selector(text=self.response.text)
            title = selector.css('.product_pod')
            for quote in title:
                data.append({
                    'name': quote.css('h3 ::attr(title)').get(),
                    'image': quote.css('.image_container a ::attr(src)').get(),
                    'star': quote.css('.star-rating Three ::text').get(),
                    'price': quote.css('.price_color::text').get(),
                    'stock': quote.css('.availability::text').get()
                })
            btn_next = selector.css('.pager .next a::attr(href)').get()
            if btn_next and self.f != 0:
                url = f'{self.url}catalogue/{btn_next}'
                self.response = requests.get(url, self.user_id)
            elif btn_next and self.f == 0:
                self.f += 1
                url = f'{self.url}{btn_next}'
                self.response = requests.get(url, self.user_id)
            else:
                break

        return data

    def print(self, data):
        print(json.dumps(data, indent=2, ensure_ascii=False))


p = Parser_git(url='https://books.toscrape.com/')
p.print(p.parse())