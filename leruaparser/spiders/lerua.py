# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leruaparser.items import LeruaparserItem
from scrapy.loader import ItemLoader

class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, text):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={text}&family=00b9b5a0-faeb-11e9-810b-878d0b27ea5b&suggest=true']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[@class = 'black-link product-name-inner']/@href").extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaparserItem(), response=response)
        loader.add_xpath('name',"//h1[@class='header-2']/text()")
        loader.add_xpath('photos',"//img[@alt='product image']/@src")
        loader.add_xpath('keys', "//dt[@class='def-list__term']/text()")
        loader.add_xpath('values', "//dd[@class='def-list__definition']/text()")
        loader.add_xpath('price', "//uc-pdp-price-view[@class = 'primary-price']/span[@slot = 'price']/text()")
        yield loader.load_item()

