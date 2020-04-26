# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import re
import os
from urllib.parse import urlparse


class LeruaparserPipeline(object):
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.lerua_photo
        self.processor = LeruaPiplineProcessing()

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        item = self.processor.get_params(item)
        collection.insert_one(item)
        return item


class LeruaPhotosPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):
        image_guid  = 'files/' + os.path.basename(urlparse(request.url).path)
#         image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'/{image_guid}.jpg'

class LeruaPiplineProcessing(object):
    def get_params(self, item):
        pattern = re.compile('\s\s+')
        values = []
        for i in item['values']:
            values.append(re.sub(pattern, '', i))
        new_list = []
        ind = 0
        while ind < len(item['keys']):
            values_key = {}
            values_key[item['keys'][ind]] = values[ind]
            new_list.append(values_key)
            item['params'] = new_list
            ind += 1
        del item['values']
        del item['keys']
        return item



    def item_completed(self, results, item, info):
       if results[0]:
            item['photos'] = [itm[1] for itm in results if itm[0]]
       return item