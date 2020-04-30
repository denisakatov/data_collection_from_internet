from lxml import html
from pprint import pprint
import requests
import re
import unicodedata
from datetime import time

pattern = re.compile('[0-9]+:[0-9]+')
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
main_link_ya = 'https://yandex.ru/news/'
link_for_concat = 'https://yandex.ru'
response = requests.get(main_link_ya, headers=header)
root = html.fromstring(response.text)
def yandex_news(root):
    link = "//a[contains(@class, 'link_theme_black')]/@href" # Xpath шаблон для списка ссылок
    text = "//a[contains(@class, 'link_theme_black')]/text()" # Xpath шаблон для текстов у ссылок
    source = "//div[@class = 'story__date']/text()" # Xpath шаблон для получения даты  и источник новосте
    result_data = root.xpath(f"{source}")
    result_data_cleared = []
    result_data_final = []
    for i in result_data:
        result_data_cleared.append(unicodedata.normalize("NFKD", i))
        for j in result_data_cleared:
            result_data_pattern = re.sub(r'\s[0-9]+:[0-9]+', '', j)
            result_data_final.append(result_data_pattern)
    link = root.xpath(f"{link}")
    links = []
    for i in link:
        links.append(link_for_concat + i)
    text = root.xpath(f"{text}")
    index = 0
    source_datas = []
    while index != len(links):
        pattern_time = result_data[index]
        pattern_time = pattern.findall(pattern_time)
        for i in pattern_time:
            h = int(i[:2])
            m = int(i[-2:])
            source_datas.append({'Title':text[index], 'TimeHour':h, 'TimeMinutes':m, 'Source': result_data_final[index], 'Link':links[index]})
        index += 1
    return source_datas

pprint(yandex_news(root))

from pymongo import MongoClient
from pprint import pprint
client = MongoClient('localhost', 27017)
db_name = 'yandex'
db = client[db_name]

def mongoDB(db, datas):
    db.insert_many(datas)
    for position in db.find():
        return(position)

yandex = db.yandex
print(mongoDB(yandex, yandex_news(root)))