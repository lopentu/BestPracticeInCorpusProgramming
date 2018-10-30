from datetime import datetime
from time import sleep
from random import random
import json

from requests import Session
from bs4 import BeautifulSoup

session = Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'


base_url = 'https://tw.appledaily.com/new/realtime/{page}'
page = 1
links = []
current_date = datetime.now().date()

while True:
    url = base_url.format(page=page)
    response = session.get(url)
    print(f'已經爬到第{page}頁')
    dom = BeautifulSoup(response.text)
    raw_time = dom.select('h1.dddd > time')[0].text
    date = datetime.strptime(raw_time, '%Y / %m / %d').date()
    if date < current_date:
        break
    elements = dom.select('h1.dddd + ul.rtddd > li')
    for element in elements:
        link = element.select('a')[0]['href']
        links.append(link)
    sleep(random() * 5)
    page += 1

base_url = 'https://tw.appledaily.com/new/realtime/{page}'
page = 1
links = []
current_date = datetime.now().date()

while True:
    url = base_url.format(page=page)
    response = session.get(url)
    print(f'已經爬到第{page}頁面')
    dom = BeautifulSoup(response.text)
    raw_time = dom.select('h1.dddd > time')[0].text
    date = datetime.strptime(raw_time, '%Y / %m / %d').date()
    if date < current_date:
        break
    elements = dom.select('h1.dddd + ul.rtddd > li')
    for element in elements:
        link = element.select('a')[0]['href']
        links.append(link)
    sleep(random() * 5)
    page += 1

htmls = []
for num, link in enumerate(links):
    print(f'還剩下{len(links) - num}個頁面')
    response = session.get(link)
    htmls.append(response.text)
    sleep(random() * 5)

posts = []
for html in htmls:
    dom = BeautifulSoup(html)
    title = dom.select('article.ndArticle_leftColumn h1')[0].text
    created_time = dom.select('article.ndArticle_leftColumn div.ndArticle_creat')[0].text
    category = dom.select('nav div.ndgTag a.current')[0].text
    content = dom.select('article.ndArticle_content p')[0].text
    post = dict(title=title, created_time=created_time, category=category, content=content)
    posts.append(post)

with open('appledaily.json', 'w') as f:
    json.dump(posts, f)
