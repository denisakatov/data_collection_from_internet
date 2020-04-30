# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import numpy as np


class JobparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.vacancies_sj_hh
        self.processor = JobparserPipelineProcessor()

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item = self.processor.distinct(item, spider)
        collection.insert_one(item)

        return item

class JobparserPipelineProcessor(object):
    def distinct(self, item, spider):
        item['max'] = np.nan
        item ['min'] = np.nan
        item ['currency'] = np.nan
        if spider.name == 'hhru':
            item = self.hhru_processor(item)
        else:
            item = self.superjob_processor(item)
        return item
    def hhru_processor(self, item):
        if len(item['salary']) != 0:
            for i in range(len(item['salary'])):
                if item['salary'][i] == 'от ':
                    item['min'] = int(item['salary'][i+1].replace('\xa0',''))
                elif (item['salary'][i] == ' до ') | (item['salary'][i] == 'до '):
                    item ['max'] = int(item['salary'][i+1].replace('\xa0',''))
                elif (item['salary'][i] == "руб.") | (item['salary'][i] == "USD") | (item['salary'][i] == "EUR"):
                    item['currency'] = item['salary'][i]
        return item

    def superjob_processor(self, item):
        if len(item['salary']) >= 2:
            for i in range(len(item['salary'])):
                if item['salary'][i] == 'до':
                    item['max'] = int(item['salary'][i+2][:-4].replace('\xa0', ''))
                    item['currency'] = item['salary'][i+2][-4:]
                elif item['salary'][i] == 'от':
                    item['min'] = int(item['salary'][i+2][:-4].replace('\xa0', ''))
                    item['currency'] = item['salary'][i+2][-4:]
                elif item['salary'][0].replace('\xa0', '').replace(' ', '').isnumeric():
                    item['min_salary'] = int(item['salary'][0].replace('\xa0', '').replace(' ', ''))
                    item['max_salary'] = int(item['salary'][1].replace('\xa0', '').replace(' ', ''))
                    item['currency'] = item['salary'][3]
        return item
