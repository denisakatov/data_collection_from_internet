from lxml import html
from pprint import pprint
import requests
import re
import datetime as DT


pattern = re.compile('\d\d\d\d\/\d+\/\d+')

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
inside_link = "https://lenta.ru/rubrics/science/"
main_link = "https://lenta.ru"
inside_links = "//li[@class='b-sidebar-menu__list-item']//a//@href"
respond = requests.get(inside_link, headers=header)
root = html.fromstring(respond.text)

def lenta(inside_links):
    respond = requests.get(inside_link, headers=header)
    root = html.fromstring(respond.text)
    pattern_text = "//div[@class='item news b-tabloid__topic_news']//a//text()"
    pattern_link = "//div[@class='item news b-tabloid__topic_news']//a//@href"
    texts = root.xpath(pattern_text)
    links = root.xpath(pattern_link)
    datas = []
    for i in links:
      data = pattern.findall(i)
      datas.append(data)
    sources = 'lenta.ru'
    final_list = []
    i = 0
    while i < len(texts):
      voc = {}
      voc['Title'] = texts[i].replace('\xa0',' ') # Название статьи
      voc['Link'] = main_link+links[i]   # Ссылка нас татью
      voc['Source'] = sources   #Источник статьи
      for data in datas[i]:
        date = DT.datetime.strptime(data, '%Y/%m/%d').date()# получаем дату новости
        voc['Data'] = str(date) # Дату преобазуем в строку, чтобы записать в базу данных
        final_list.append(voc)
      i += 1
    return final_list

# Далее цикл для того, чтобы применить функцию на каждой странице самоой новости, а полученную переменную запишем в единую базу мейли и лента.
for i in root.xpath(inside_links) [1:13]: # В отобранных данных есть ссылки на главную страницу и на другой сайт (с одинаковыми символами). Поэтому возьмем срез.
    root = main_link+i
    list_pages = lenta(root)

# Для mail и lenta выводим одинаковые данные, поэтому можно записать в одну базу

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_name = 'lenta'
db = client[db_name]

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_name = 'mail_lenta'
db = client[db_name]

def mongoDB(db, datas):
    db.insert_many(datas)
    for position in db.find():
        return(position)

mail_lenta = db.mail_lenta
print(mongoDB(mail_lenta, list_pages))