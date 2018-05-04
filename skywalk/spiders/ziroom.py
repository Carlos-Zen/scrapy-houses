# -*- coding: utf-8 -*-
import json

import scrapy
from skywalk.items import *
from skywalk.utils import *
from skywalk.dict import *
import datetime

REG = {
    'number': r'(\d+)',
    'yuan': r'(\d+)元',
    'huxing': r'(\d)室(\d)?厅?(\d)?卫?',
    'floor': r'(\d+)\/(\d+)',
    'rent_type': r'(.租)',
    'payment': r'押(.)付(.)',
    'district_block': r'(.+?)\s+\-\s+(.+)',
    'longi': r'.*longitude\s?:\s?\'(-?\d+\.\d+)\'',
    'lati': r'.*latitude\s?:\s?\'(-?\d+\.\d+)\'',
    'city': r'.*var\s+city_name\s?=\s?\'(.*)\';',
    'price': r'(\d+).*?(\d+)',
    'norns': r'[^\r\n\s]+',
    'rm_url_params': r'(.*)\?.*',
    'bathroom': r'(独立?卫(生间)?)',
    'balcony': r'(独立?阳台)',
    'orientation': r'\s(.*)',
}


class ZiroomSpider(scrapy.Spider):
    name = 'ziroom'
    allowed_domains = ['ziroom.com']
    start_urls = []
    custom_settings = {
        # 'CLOSESPIDER_ERRORCOUNT': 100,
        'DOWNLOAD_DELAY': 0.28,
        # 'CONCURRENT_REQUESTS': 1,
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
            yield scrapy.Request(response.url + '?p=' + str(i), self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("ul#houseList a.t1::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)
            # test
        # for page_link in ['http://sh.ziroom.com/z/vr/61178049.html']:
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
        house['title'] = trim(response.css('div.room_name  h2::text').extract_first())

        house['city'] = response.css('span#curCityName::text').extract_first()
        house['district'] = response.css('div.node_infor a')[1].css('::text').re_first(r'(.*).租')
        house['block'] = response.css('div.node_infor a')[2].css('::text').re_first(r'(.*)公寓出租')
        house['apartment'] = response.css('div.node_infor a')[3].css('::text').re_first(r'(.*)租房信息')

        house['rental'] = int(response.css('span#room_price::text').re_first(REG['number']))

        house['pictures'] = response.css("ul.lof-main-wapper img::attr(src)").extract()

        rent_type = response.css('div.node_infor a')[1].css('::text').re_first(r'.*(.租)')
        house['rent_type'] = v2k('rent_type', rent_type)

        house['room_area'] = int(response.css('ul.detail_room li')[0].css('::text').re_first(REG['number']))
        house['orientation'] = response.css('ul.detail_room li')[1].css('::text').re_first(REG['orientation'])
        huxing = response.css('ul.detail_room li')[2].css('::text').re(
            REG['huxing'])
        try:
            house['room_num'] = int(huxing[0])
            house['hall_num'] = int(huxing[1])
            house['bathroom_num'] = int(huxing[2])
        except Exception:
            pass

        try:
            house['floor'], house['building_floor'] = response.css('ul.detail_room li')[3].css('::text').re(
                r'(\d+)\/(\d+)')
        except Exception:
            pass
        try:
            house['traffic'] = trim(response.css('ul.detail_room li')[4].css('span::text').extract_first())
        except Exception:
            pass


        house['content'] = response.css("div.aboutRoom").extract_first()
        house['features'] = response.css("p.room_tags span::text").extract()
        try:
            if len(response.css("p.room_tags span::text").re(REG['bathroom'])) > 0: house['exclusive_bathroom'] = 1
            if len(response.css("p.room_tags span::text").re(REG['balcony'])) > 0: house['exclusive_balcony'] = 1
        except Exception:
            pass

        house['public_falicities'] = response.css("ul.configuration li::text").extract()
        # longti,lati
        house['longi'] = response.css('input#mapsearchText::attr(data-lng)').extract_first()
        house['lati'] = response.css('input#mapsearchText::attr(data-lat)').extract_first()
        house['position'] = {
            'type': 'Point',
            'coordinates': [float(house['longi']), float(house['lati'])]
        }
        # 固定付款方式
        house['payment_deposit'] = 1
        house['payment_rental'] = 3
        house['service_fee'] = int(house['rental'] * 1.2)

        house['uniqe_key'] = uniqe_key(house)
        house['house_key'] = house_key(house)
        # date and unique_key
        house['crawl_date'] = datetime.datetime.now()
        house['uniqe_key_no_date'] = create_uniqe_key(house)
        # collection_name
        house['collection'] = get_collection_name(house['city'])
        house['source_url'] = response.url
        yield house
