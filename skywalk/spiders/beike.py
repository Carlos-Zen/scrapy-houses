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
    'longi': r'.*____json4fe\.lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati': r'.*____json4fe\.lat\s?=\s?\'(-?\d+\.\d+)\';',
    'city': r'.*var\s+city_name\s?=\s?\'(.*)\';',
    'price': r'(\d+).*?(\d+)',
    'norns': r'[^\r\n\s]+',
    'rm_url_params': r'(.*)\?.*'
}


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['ke.com']
    start_urls = []
    custom_settings = {
        # 'CLOSESPIDER_ERRORCOUNT': 100,
        'DOWNLOAD_DELAY': 0.68,
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
        for i in range(1,self.total_page):
            yield scrapy.Request(response.url + 'pg' + str(i) + '/', self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("div.content__list a.link::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)

    def parse_page(self, response):
        '''
        解析内容
        '''

        # 通过url判断，该房源是集中式公寓品牌页面还是普通页面,区分

        if response.url.find('apartment') is not -1:
            #集中式公寓单页面返回多个房型
            for house in self.parse_apartment_page(response):
                yield house
        else:
            yield self.parse_normal_page(response)

    def parse_spacial_page(self, response, house):
        """
        集中式公寓页面规则
        :param response:
        :param house:
        :return:
        """
        houses_json_string = response.css('script').re_first(r'JSON\.stringify\((.*)\)\)')
        houses = json.loads(houses_json_string)
        for one_house in houses['layout_list']:

            house = HouseItem()
            house['rent_type'] = 3  # 公寓
            house['source_from'] = self.name
            house['branch'] = response.css('p.content__aside--title span::text').extract_first()
            house['brand'] = houses['apartment_name']
            house['style'] = one_house['name']
            # title = 品牌 + 分店 + 房型
            house['title'] = house['brand'] + response.css('p.content__aside--title span::text').extract_first() + house['style']

            house['rental'], house['rental_limit'] = one_house['min_price'], one_house['max_price']
            house['empty_house_num'] = one_house['rentable_num']
            house['room_area'] = one_house['min_area']
            house['private_falicities'] = [ f['name'] for f in one_house['facility'] ]
            house['pictures'] = [ p['picture_url'] for p in one_house['detail_picture'] ]

            house['city'] = response.css('head title::text').re_first(r'-(.*)贝壳找房')

            house['address'] = response.css("div.flat__info--desc p.flat__info--subtitle::text").re_first(REG['norns'])

            house['content'] = response.css("div.flat__info--desc p.flat__info--description::text").extract_first()
            house['public_falicities'] = response.css("div.flat__info--facilities li::text").extract()
            # longti,lati
            house['longi'] = houses['longitude']
            house['lati'] = houses['latitude']
            house['position'] = {
                'type': 'Point',
                'coordinates': [float(house['longi']), float(house['lati'])]
            }
            month = time.strftime("%Y-%m", time.localtime())
            house['uniqe_key'] = create_uniqe_key(house, [month])

            # date and unique_key
            house['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
            house['uniqe_key_no_date'] = create_uniqe_key(house)
            # collection_name
            house['collection'] = get_collection_name(house['city'])
            yield house

    def parse_normal_page(self, response):
        """
        普通页面规则
        :param response:
        :param house:
        :return:
        """
        house = HouseItem()
        house['source_from'] = self.name
        house['title'] = response.css('div.housedetail h2::text').extract_first()
        house['brand'] = response.css('div.apartment-info span::text').extract_first()
        house['publish_date'] = response.css('div.tags span::text').re_first(r'.*(\d{4}[-\/]\d{2}[-\/]\d{2})')

        house['city'] = response.css('div.crumbar a')[0].css('::text').re_first(r'(.*)公寓')
        house['district'] = response.css('div.crumbar a')[1].css('::text').re_first(r'(.*)公寓')
        house['block'] = response.css('div.crumbar a')[2].css('::text').re_first(r'(.*)公寓')

        rent_type = response.css("ul.house-info-list li")[1].re_first(
            REG['rent_type'])
        house['rent_type'] = v2k('rent_type', rent_type)
        house['features'] = response.css('ul.tags-list li.tag::text').extract()
        house['rental'] = response.css('div.detail_header span.price::text').extract_first()

        area = response.css("ul.house-info-list li")[0].re_first(REG['number'])
        house['room_area'] = area
        if rent_type == '整租':
            house['house_area'] = area
        house['room_num'], house['hall_num'], house['bathroom_num'] = response.css("ul.house-info-list li")[1].css(
            'span').re(
            REG['huxing'])

        house['orientation'] = response.css("ul.house-info-list li")[1].css('span').css('::text').re_first(
            r'.*?\s+(.*?)\s+')
        house['floor'], house['building_floor'] = response.css("ul.house-info-list li")[2].css('span').css('::text').re(
            r'(\d+)\/(\d+)')

        house['address'] = response.css("ul.house-info-list li")[3].css('span').css('::text').extract_first()
        try:
            house['traffic'] = response.css("ul.house-info-list li")[4].css('span').css('::text').extract_first()
        except Exception:
            pass

        house['content'] = response.css("div.desc-wrap p#desc::text").extract_first()
        house['private_falicities'] = response.css("div.house-setup li::text").re(REG['configure'])

        # pictures
        house['pictures'] = response.css("ul#title-img-list img::attr(src)").re(REG['rm_url_params'])
        # longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])
        house['position'] = [house['longi'], house['lati']]

        month = time.strftime("%Y-%m", time.strptime(house['publish_date'], "%Y-%m-%d"))
        house['uniqe_key'] = create_uniqe_key(house, [month])
        # date and unique_key
        house['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
        house['uniqe_key_no_date'] = create_uniqe_key(house)
        # collection_name
        house['collection'] = get_collection_name(house['city'])
        return house