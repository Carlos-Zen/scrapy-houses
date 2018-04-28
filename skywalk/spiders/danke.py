# -*- coding: utf-8 -*-
import json

import scrapy
from skywalk.items import *
from skywalk.utils import *
from skywalk.dict import *
import time

REG = {
    'number': r'(\d+)',
    'yuan': r'(\d+)元',
    'huxing': r'(\d)室(\d)?厅?(\d)?卫?',
    'floor': r'(\d+)\/(\d+)',
    'rent_type': r'(.租)',
    'payment': r'押(.)付(.)',
    'district_block': r'(.+?)\s+\-\s+(.+)',
    'coodinates': r'.*var\s+map\s?=\s?new\sBaiduDetailMap\((.*?)\,(.*?)\,.*',
    'city': r'.*var\s+city_name\s?=\s?\'(.*)\';',
    'price': r'(\d+).*?(\d+)',
    'norns': r'[^\r\n\s]+',
    'rm_url_params': r'(.*)\?.*',
    'bathroom': r'(独立?卫(生间)?)',
    'balcony': r'(独立?阳台)',
    'orientation': r'\s(.*)',
}


class DankeSpider(scrapy.Spider):
    name = 'danke'
    allowed_domains = ['dankegongyu.com']
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 0.28,
    }
    total_page = 200

    def start_requests(self):
        self.start_urls = self.settings.get('START_URLS')[self.name]
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        '''
        解析列表分页
        '''
        if self.settings.get('CRAWL_PAGE') > 0: self.total_page = self.settings.get('CRAWL_PAGE')
        for i in range(1, self.total_page):
            yield scrapy.Request(response.url + '?page=' + str(i), self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("div.r_ls_box div.r_lbx a.rimg::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)
        # test
        # for page_link in ['https://www.dankegongyu.com/room/1425952751.html']:
        #     yield response.follow(page_link, self.parse_page)

    def parse_page(self, response):
        """
        普通页面规则
        :param response:
        :param house:
        :return:
        """
        house = HouseItem()

        house['source_from'] = self.name
        house['brand'] = self.name
        # title = 品牌 + 分店 + 房型
        house['title'] = trim(response.css('div.room-detail  div.room-name h1::text').extract_first())

        house['city'] = response.css('span#dropdownMenu1::text').extract_first()
        house['district'] = response.css('div.detail-roombox a')[0].css('::text').extract_first()
        house['block'] = response.css('div.detail-roombox a')[1].css('::text').extract_first()
        house['apartment'] = response.css('div.detail-roombox a')[2].css('::text').extract_first()

        house['rental'] = int(response.css('div.room-price-sale::text').extract_first())

        house['pictures'] = response.css("div.carousel-inner img::attr(src)").extract()

        rent_type = response.css('b.methodroom-rent::text').extract_first() + '租'
        house['rent_type'] = v2k('rent_type', rent_type)

        house['room_area'] = int(
            response.css('div.room-detail-box div.room-list label')[0].css('::text').re_first(REG['number']))
        house['orientation'] = response.css('div.room-detail-box div.room-list label')[4].css('::text').re_first(
            r'：(.*)')
        huxing = response.css('div.room-detail-box div.room-list label')[2].css('::text').re(
            REG['huxing'])
        try:
            house['room_num'] = int(huxing[0])
            house['hall_num'] = int(huxing[1])
            house['bathroom_num'] = int(huxing[2])
        except Exception:
            pass

        try:
            house['floor'], house['building_floor'] = response.css('div.room-detail-box div.room-list label')[5].css(
                '::text').re(
                r'(\d+)\/(\d+)')
        except Exception:
            pass
        try:
            house['traffic'] = response.css('div.room-detail-box div.room-list label')[7].css('::text').re_first(r'：(.*)')
            house['address'] = house['traffic']
        except Exception:
            pass

        try:
            house['features'] = response.css("div.room-detail-right div.room-title span::text").extract()
            if len(response.css("div.room-detail-right div.room-title span::text").re(REG['bathroom'])) > 0: house[
                'exclusive_bathroom'] = 1
            if len(response.css("div.room-detail-right div.room-title span::text").re(REG['balcony'])) > 0: house[
                'exclusive_balcony'] = 1
        except Exception:
            pass

        # longti,lati
        house['longi'], house['lati'] = response.css('script').re(
            r'.*var\s+map\s?=\s?new\sBaiduDetailMap\((.*?)\,(.*?)\,.*')[:2]
        house['position'] = {
            'type': 'Point',
            'coordinates': [float(house['longi']), float(house['lati'])]
        }
        house['payment_deposit'] = 1
        house['payment_rental'] = 1
        house['service_fee'] = int(house['rental'] * 1.05)

        house['uniqe_key'] = uniqe_key(house)
        house['house_key'] = house_key(house)
        # date and unique_key
        house['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
        house['uniqe_key_no_date'] = create_uniqe_key(house)
        # collection_name
        house['collection'] = get_collection_name(house['city'])
        yield house
