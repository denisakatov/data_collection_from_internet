"""1) Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайта superjob.ru и hh.ru. Приложение должно анализировать несколько страниц сайта(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
        *Наименование вакансии
        *Предлагаемую зарплату (отдельно мин. и отдельно макс.)
        *Ссылку на саму вакансию
        *Сайт откуда собрана вакансия
По своему желанию можно добавить еще работодателя и расположение. Данная структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas."""

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

d = pattern.findall(hh_pages)
max_p = int(max(d))
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
        hh_link = i.find('a')['href']
        vacancies_voc = {}
        vacancies_voc['Работодатель'] = hh_employer.replace('\xa0','')
        vacancies_voc['Позиция'] = hh_position
        vacancies_voc['Ссылка'] = hh_link
        vacancies_voc['Описание'] = hh_short_description
        vacancies_voc['Зарплата'] = hh_salary
        vacancies.append(vacancies_voc)
        index += 1
    max_p -= 1
print(f'Количество вакансий {len(vacancies)}') # Смотрим количество вакансий
pprint(vacancies)

print('-'*50)
#print(sal)
#Далее обработаем зарплату. Выведем минимальную и максимальную зарплаты в зависимости от валюты, но без учета 'от' и 'до'.
rub1 = []
eur1 = []
usd1 = []
for i in sal:
    if len(i) > 1:
        if i[-1] == 'руб.':
            rub1.append(i[-2].split('-'))
        elif i[-1] == 'EUR':
            eur1.append(i[-2].split('-'))
        elif i[-1] == 'USD':
            usd1.append(i[-2].split('-'))
    else:
        None
print('*'*50)

rub = []
eur = []
usd = []
for i in rub1:
    for j in i:
        rub.append(int(j))
for i in eur1:
    for j in i:
        eur.append(int(j))
for i in usd1:
    for j in i:
        usd.append(int(j))
print(sorted(rub)) # Отсортируем рубли только для проверки
print(f'Минимальная зарплата в рублях {min(rub)}, Максимальная зарплата в рублях {max(rub)}')
print(eur) #Выводим весь список евро для проверки
print(f'Минимальная зарплата в евро {min(eur)}, Максимальная зарплата в евро {max(eur)}')
print(usd) #Выводим весь список длолларов для проверки
print(f'Минимальная зарплата в долларах {min(usd)}, Максимальная зарплата в долларах {max(usd)}')
