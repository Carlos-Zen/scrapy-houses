# coding: utf-8

import scrapy

class TestSpider(scrapy.Spider):
    name = 'test'
    custom_settings = {
        # 'CLOSESPIDER_ERRORCOUNT': 20,
        'DOWNLOAD_DELAY': 2.38,
        'CONCURRENT_REQUESTS': 1,
    }
    total_page = 100

    def start_requests(self):
        self.start_urls = [
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
            'http://control.uuzu.com/api/game',
                           ]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in range(1,self.total_page):
            yield scrapy.Request(response.url + '?p=' + str(i) + '/', self.parse_page_url)

    def parse_page_url(self, response):
        return {"test":"test"}