# -*- coding: utf-8 -*-
import scrapy


class A58pinpaiSpider(scrapy.Spider):
    name = '58pinpai'
    allowed_domains = ['58.com']
    start_urls = ['http://58.com/']

    def parse(self, response):
        pass
