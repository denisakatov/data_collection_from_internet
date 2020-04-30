import requests
from lxml import html
from pprint import pprint
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient

options = Options()
options.add_argument('--headless')

driver = webdriver.Chrome(options=options)
driver.get('https://www.mvideo.ru/')
just_offer = driver.find_element_by_xpath("//div[@data-init= 'gtm-push-products']")

while True:
    try:
        button = WebDriverWait(just_offer, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-btn")))
        button.click()
    except Exception as e:
        break
goods = just_offer.find_elements_by_class_name('sel-product-tile-title')
result = []
for good in goods:
    result.append(good.get_attribute("data-product-info"))

def form_list(result):
  i = 0
  final_list = []
  while len(result) != i:
    new_voc = {}
    json_result = json.loads(result[i])
    final_list.append(json_result)
    i += 1
  return final_list

client = MongoClient('localhost', 27017)
for item in form_list(result):
    try:
        client['mvideo']['goods'].insert_one(item)
    except DuplicateKeyError:
        pass

driver.quit()