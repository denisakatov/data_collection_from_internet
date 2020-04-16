import re
import requests
from pprint import pprint
from bs4 import BeautifulSoup as bs

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
index = 0
main_link = 'https://kaliningrad.hh.ru/search/vacancy?L_is_autosearch=false&area=113&clusters=true&enable_snippets=true&text=python&page={index}'
response = requests.get(main_link,headers=headers).text
soup = bs(response, 'lxml')
vacancy_blocks = soup.find('div', {'class': 'vacancy-serp'})
vacancy_block = vacancy_blocks.find_all('div', {'class': 'vacancy-serp-item'})

# Далее ищем максимальное количество страниц выбранных вакансий
hh_pages = soup.findChild('div', {'data-qa': 'pager-block'}).getText()
pattern = re.compile('\d+')
pattern_id = re.compile('\/\d+\?')

d = pattern.findall(hh_pages)
max_p = int(max(d))
#max_p = 1

print(f'Количество страниц {max_p}') # Для проверки выведем количество страниц
vacancies = []
sal=[]
#Выбираем даннные:
while max_p != 0:
    for i in vacancy_block:
        hh_employer = i.find('div',{'class':'vacancy-serp-item__meta-info'}).getText()
        hh_position = i.find('a',{'class':'bloko-link HH-LinkModifier'}).getText()
        hh_short_description = i.find('div',{'class':'g-user-content'}).getText()
        hh_salary = i.find('div',{'class':'vacancy-serp-item__sidebar'}).getText().replace('\xa0','')
        hh_salary_split = hh_salary.split(' ')
        sal.append(hh_salary_split)
        hh_link = i.find('a',{'class':'bloko-link HH-LinkModifier'})['href']
        id = str(pattern_id.findall(hh_link))

        vacancies_voc = {}
        vacancies_voc['id'] = pattern.findall(id)
        vacancies_voc['Employer'] = hh_employer.replace('\xa0','')
        vacancies_voc['Position'] = hh_position
        vacancies_voc['Link'] = hh_link
        vacancies_voc['Description'] = hh_short_description
        #vacancies_voc['Salary_on_site'] = hh_salary
        for i in sal:
            salary_from = None
            salary_to = None
            currency = None
            if len(i) == 2:
                salary_from = int(i[0].split('-')[0])
                salary_to = int(i[0].split('-')[1])
                currency = i[-1]
            elif len(i) == 3:
                if i[0] == 'от':
                    salary_from = int(i[1])
                    currency = i[-1]
                elif i[0] == 'до':
                    salary_to = int(i[1])
                    currency = i[-1]
        vacancies_voc['Currency'] = currency
        vacancies_voc['Salary_from'] = salary_from
        vacancies_voc['Salary_to'] = salary_to
        vacancies.append(vacancies_voc)
        index += 1
    max_p -= 1
#pprint(vacancies)

from pymongo import MongoClient
from pprint import pprint
client = MongoClient('localhost', 27017)
collection_name = 'new'
db = client[collection_name]
hh_positions = db.positions
#hh_positions.drop() #  Если надо базу очистить

def hh_base(hh_positions, datas):
    hh_positions.insert_many(datas)
    for position in hh_positions.find():
        return(position)

def filter_of_salary(ind):
    count = 0
    hh_vocabluary = []
    for hh in hh_positions.find({'Salary_to':{'$gte': ind}},{'_id':0}):
        count +=1
        hh_vocabluary.append(hh)
    print(f'Найдено вакансий: {count}')
    return hh_vocabluary

hh_base(hh_positions, vacancies)
ind = int (input('Введите максимально желаемую зарплату: '))
pprint(filter_of_salary(ind))
