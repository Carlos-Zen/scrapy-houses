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
    'longi': r'.*longitude\s?:\s?\'(-?\d+\.\d+)\'',
    'lati': r'.*latitude\s?:\s?\'(-?\d+\.\d+)\'',
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
        for i in range(1, self.total_page):
            yield scrapy.Request(response.url + 'pg' + str(i) + '/', self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("div.content__list a.link::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)
        #test
        # for page_link in ['http://sh.zu.ke.com/zufang/SH1975106301742817280.html']:
        #     yield response.follow(page_link, self.parse_page)


    def parse_page(self, response):
        '''
        解析内容
        '''

        # 通过url判断，该房源是集中式公寓品牌页面还是普通页面,区分

        if response.url.find('apartment') is not -1:
            # 集中式公寓单页面返回多个房型
            for house in self.parse_apartment_page(response):
                yield house
        else:
            yield self.parse_normal_page(response)

    def parse_apartment_page(self, response):
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
            house['title'] = house['brand'] + response.css('p.content__aside--title span::text').extract_first() + \
                             house['style']

            house['rental'], house['rental_limit'] = int(one_house['min_price']), int(one_house['max_price'])
            house['empty_house_num'] = int(one_house['rentable_num'])
            house['room_area'] = int(one_house['min_area'])
            house['private_falicities'] = [f['name'] for f in one_house['facility']]
            house['pictures'] = [p['picture_url'] for p in one_house['detail_picture']]

            house['city'] = response.css('head title::text').re_first(r'-(.*)贝壳找房')

            house['address'] = response.css("div.flat__info--desc p.flat__info--subtitle::text").re_first(REG['norns'])

            house['content'] = trim(response.css("div.flat__info--desc p.flat__info--description::text").extract_first())
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
            house['multi'] = 1
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
        house['brand'] = trim(response.css('p.content__aside__list--subtitle::text').extract_first())
        # title = 品牌 + 分店 + 房型
        house['title'] = response.css('div.content  p.content__title::text').extract_first()

        house['city'] = response.css('div.bread__nav a')[0].css('::text').re_first(r'(.*)贝壳找房')
        house['district'] = response.css('div.bread__nav a')[1].css('::text').re_first(r'(.*)租房')
        house['block'] = response.css('div.bread__nav a')[2].css('::text').re_first(r'(.*)租房')
        house['apartment'] = response.css('div.bread__nav a')[3].css('::text').re_first(r'(.*)租房')

        house['rental'] = int(response.css('div.content__aside  p.content__aside--title span::text').extract_first())

        house['pictures'] = response.css("ul.content__article__slide__wrapper img::attr(src)").re(REG['rm_url_params'])

        rent_type = response.css('p.content__article__table span')[0].css('::text').extract_first()
        house['rent_type'] = v2k('rent_type', rent_type)
        house['room_area'] = response.css('p.content__article__table span')[2].css('::text').re_first(REG['number'])
        huxing = response.css('p.content__article__table span')[
            1].css('::text').re(
            REG['huxing'])
        try:
            house['room_num'] = int(huxing[0])
            house['hall_num'] = int(huxing[1])
            house['bathroom_num'] = int(huxing[2])
        except Exception:
            pass

        house['room_area'] = response.css('p.content__article__table span')[3].css('::text').extract_first()
        house['floor'], house['building_floor'] = response.css("div.content__article__info li")[7].css('::text').re(
            r'(\d+)\/(\d+)')
        house['content'] = response.css("div#desc p.threeline::text").extract_first()


        house['public_falicities'] = response.css("ul.content__article__info2 li::text").extract()
        # longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])
        house['position'] = {
            'type': 'Point',
            'coordinates': [float(house['longi']), float(house['lati'])]
        }

        house['publish_date'] = response.css('div.content__article__info li')[1].css('::text').re_first(r'.*(\d{4}[-\/]\d{2}[-\/]\d{2})')
        month = time.strftime("%Y-%m", time.strptime(house['publish_date'], "%Y-%m-%d"))
        house['uniqe_key'] = create_uniqe_key(house, [month])

        # date and unique_key
        house['crawl_date'] = time.strftime("%Y-%m-%d", time.localtime())
        house['uniqe_key_no_date'] = create_uniqe_key(house)
        # collection_name
        house['collection'] = get_collection_name(house['city'])
        return house
