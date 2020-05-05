# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst,MapCompose

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def cleaner_price(values):
    if values:
        return int(values)
    return values

class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    keys = scrapy.Field()
    values = scrapy.Field()
    params = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(cleaner_price))


