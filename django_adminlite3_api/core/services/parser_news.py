import time
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from selenium.webdriver.chrome.service import Service
from selenium import webdriver

from core.models import Post

ROOT_URL_YANDEX = 'https://market.yandex.ru'
URL_YANDEX = 'https://market.yandex.ru/partners/news'

URL_OZON = 'https://seller.ozon.ru/content-api/news/?_limit=10&_start=0'
headers = {
    "Accept": "/*/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/100.0.4896.75 Safari/537.36",
}

months = {'января': '01', 'февраля': '02', 'марта': '03', 'апреля': '04', 'мая': '05', 'июня': '06',
          'июля': '07', 'августа': '08', 'сентября': '09', 'октября': '10', 'ноября': '11', 'декабря': '12'}


def format_date(date: str) -> str:
    date = date.split()
    date = [date[-1], months.get(date[-2]), date[-3]]
    date = '-'.join(date)
    return date


def get_news_yandex():
    response = requests.get(URL_YANDEX, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    raw_news = soup.find_all('div', class_="news-list__item")[:10]
    links_raw_news = [link.find('a').get('href') for link in raw_news]
    for link in links_raw_news:
        URL = ROOT_URL_YANDEX + link
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        tags = soup.find('div', class_="news-info__tags").text
        tags = tags.split("#")[1:]
        title = soup.find('div', class_="news-info__title").text
        date = format_date(soup.find('time', class_="news-info__published-date").text)
        data = {'title': title, 'resource': 'Yandex', 'created_at': date}
        print(data)
        post = Post.objects.create(**data)
        post.tags.add(*tags)


def get_news_ozon():
    service = Service("C:\\chromedriver\chromedriver.exe")
    options = webdriver.ChromeOptions()
    browser = webdriver.Chrome(service=service, options=options)
    browser.get(URL_OZON)
    main_page = browser.page_source
    soup = BeautifulSoup(main_page, 'lxml')
    json_raw = soup.find('pre').text
    json_clean = json.loads(json_raw)
    for dict in json_clean:
        title = dict.get('title')
        date = dict.get('date').split('T')[0]
        if dict.get('theme'):
            tags = [tag.get('name') for tag in dict.get('theme')]
        data = {'title': title, 'resource': 'Ozon', 'created_at': date}
        post = Post.objects.create(**data)
        post.tags.add(*tags)

