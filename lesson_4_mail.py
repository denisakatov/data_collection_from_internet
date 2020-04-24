from lxml import html
from pprint import pprint
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
main_link = "https://news.mail.ru"

def mail(main_link):
    respond = requests.get(main_link, headers=header)
    root = html.fromstring(respond.text)
    pattern_text = "//a[@class='link link_flex']//text()"
    pattern_link = "//a[@class='link link_flex']//@href"
    texts = root.xpath(pattern_text)
    links = root.xpath(pattern_link)
    final_list = []
    i = 0
    while i < len(texts): #запускаем цикл, чтобы по индексу вставлять в словарь сообветствующие элементы
        voc = {}
        voc['Title'] = texts[i].replace('\xa0',' ') #Получаем текст. Убираем ненужные пробельные символы
        new_link = main_link+links[i] #Конкатенируем строки
        voc['Link'] = new_link #Получаем ссылки
        respond = requests.get(new_link, headers=header)# Далее строчки для получения источника уже на странице новости.
        root_source = html.fromstring(respond.text)
        pattern_source = "//a[@class='link color_gray breadcrumbs__link']//text()"
        source = root_source.xpath(pattern_source)
        source = ''.join(source) # Список преобразуем в строку
        voc['Source'] = source
        voc['Data'] = None # На свежих страницах написано сколько часов назад была статья напечатаноа. Не проеобразовывал. Можно было по подобию получения источника новостей.
        final_list.append(voc)
        i += 1
    return final_list
print(mail(main_link))


# Для mail и lenta выводим одинаковые данные, поэтому можно записать в одну базу
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db_name = 'mail_lenta'
db = client[db_name]

def mongoDB(db, datas):
    db.insert_many(datas)
    for position in db.find():
        return(position)

mail_lenta = db.mail_lenta
print(mongoDB(mail_lenta, mail(main_link)))

