from pprint import pprint
import requests
from lxml import html
from pymongo import MongoClient


header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}
news = []
client = MongoClient('127.0.0.1',27017)
db = client['news']
jj = db.news


#****LENTARU****
link = 'https://lenta.ru'
response_lenta = requests.get(link)
dom = html.fromstring(response_lenta.text)


news_title = dom.xpath("//section[contains(@class,'b-top7-for-main')]//a[contains(@href,'news')]/text()")
news_origin = dom.xpath("//section[contains(@class,'b-top7-for-main')]//span[@class='mg-card-source__source']/a/text()")
news_link = dom.xpath("//section[contains(@class,'b-top7-for-main')]//a[contains(@href,'news')]/@href")
news_date = dom.xpath("//section[contains(@class,'b-top7-for-main')]//time/@datetime")

for n in range(len(news_title)-1):

    elements={}

    elements['title'] = news_title[n]
    elements['date'] = news_date[n]
    elements['link'] = link + news_link[n+1]
    elements['origin'] = link

    news.append(elements)


#****YANDEXNEWS****
response_yandex = requests.get('https://yandex.ru/news')

dom = html.fromstring(response_yandex.text)
items = dom.xpath("//article")


for item in items:
    #news_resp = requests.get(item)
    #news_dom = html.fromstring(news_resp.text)
    elements={}

    news_title = item.xpath(".//a[@class='news-card__link']//text()")
    news_origin = item.xpath(".//span[@class='mg-card-source__source']/a/text()")
    news_link = item.xpath(".//a[@class='news-card__link']/@href")
    news_date = item.xpath(".//span[@class='mg-card-source__time']/text()")

    elements['title'] = news_title[0]
    elements['date'] = news_date[0]
    elements['link'] = news_link[0]
    elements['origin'] = news_origin[0]

    news.append(elements)

#****NEWSMAILRU****
response_mail = requests.get('https://news.mail.ru/')
dom = html.fromstring(response_mail.text)
items = dom.xpath("//a[contains(@class,'js-topnews__item')]/@href")

for item in items:
    news_resp = requests.get(item)
    news_dom = html.fromstring(news_resp.text)
    elements={}

    news_title = news_dom.xpath("//h1/text()")
    news_origin = news_dom.xpath("//a[@class='link color_gray breadcrumbs__link']//text()")
    news_link = item
    news_date = news_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")

    elements['title'] = news_title[0]
    elements['date'] = news_date[0]
    elements['link'] = news_link[0]
    elements['origin'] = news_origin[0]

    news.append(elements)

jj.insert_many(news)
ttl_news = len(news)
print('Сохранено в базу', ttl_news, 'новостей')
