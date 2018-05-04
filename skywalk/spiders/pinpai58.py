# -*- coding: utf-8 -*-
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
    'longi': r'.*____json4fe\.lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati': r'.*____json4fe\.lat\s?=\s?\'(-?\d+\.\d+)\';',
    'city': r'.*var\s+city_name\s?=\s?\'(.*)\';',
    'price': r'(\d+).*?(\d+)',
    'configure': r'[^\r\n\s]+',
    'rm_url_params': r'(.*)\?.*'
}


class Pinpai58Spider(scrapy.Spider):
    name = 'pinpai58'
    allowed_domains = ['58.com']
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 1.18,
        'CONCURRENT_REQUESTS': 2,
    }
    total_page = 100

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
            yield scrapy.Request(response.url + 'pn/' + str(i) + '/', self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("ul.list li a::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)

    def parse_page(self, response):
        '''
        解析内容
        '''
        house = HouseItem()
        house['source_from'] = self.name


        # 通过字段判断，该房源是集中式公寓品牌页面还是普通页面,区分
        special_title = response.css('p.head-title::text').extract_first()
        if special_title:
            self.parse_spacial_page(response, house)
        else:
            self.parse_normal_page(response, house)

        # date and unique_key
        house['crawl_date'] = datetime.datetime.now()
        house['uniqe_key_no_date'] = create_uniqe_key(house)
        # collection_name
        house['collection'] = get_collection_name(house['city'])
        yield house

    def parse_spacial_page(self, response, house):
        """
        集中式公寓页面规则
        :param response:
        :param house:
        :return:
        """
        house['title'] = response.css('p.head-title::text').extract_first()
        house['brand'] = house['title']
        house['rent_type'] = 3  # 公寓
        house['branch'] = response.css('p.head-address::text').extract_first()
        house['apartment'] = house['title']

        house['city'] = response.css('div.curmbar a')[0].css('::text').re_first(r'(.*)公寓')
        house['district'] = response.css('div.curmbar a')[1].css('::text').re_first(r'(.*)公寓')
        house['block'] = response.css('div.curmbar a')[2].css('::text').re_first(r'(.*)公寓')

        house['style'] = response.css('div.house-title div.housedetail span.bt::text').extract_first()
        house['empty_house_num'] = response.css('div.house-title div.housedetail span.houseNum::text').re_first(
            REG['number'])
        house['features'] = response.css('ul.tags-list li.tag::text').extract()
        prices = response.css('div.detailMoney span.price::text').re(REG['price'])

        try:
            house['rental'] = int(prices[0])
            house['rental_limit'] = int(prices[1])
        except Exception:
            pass

        payment_rental, payment_deposit = response.css('div.detailMoney span.deposit::text').re(REG['payment'])
        house['payment_deposit'],house['payment_rental'] = chinese_to_arabic(payment_rental), chinese_to_arabic(
            payment_deposit)
        house['room_num'], house['hall_num'], house['bathroom_num'] = response.css("div.detailHX span::text").re(
            REG['huxing'])
        house['room_area'] = int(response.css("div.detailArea span::text").re_first(REG['number']))
        house['orientation'] = response.css("div.detailCX span::text").extract_first()
        house['address'] = response.css("div.detailAddress span::text").extract_first()

        house['content'] = trim(response.css("div.describe-descri p.desc::text").extract_first())
        house['private_falicities'] = response.css("div.house-configure li::text").re(REG['configure'])
        # pictures
        house['pictures'] = response.css("ul#leftImg img::attr(src)").re(REG['rm_url_params'])

        # longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])
        house['position'] = {
            'type': 'Point',
            'coordinates': [float(house['longi']), float(house['lati'])]
        }
        house['uniqe_key'] = uniqe_key(house)
        house['source_url'] = response.url

    def parse_normal_page(self, response, house):
        """
        普通页面规则
        :param response:
        :param house:
        :return:
        """
        house['title'] = response.css('div.housedetail h2::text').extract_first()
        house['brand'] = response.css('div.apartment-info span::text').extract_first()
        house['publish_date'] = response.css('div.tags span::text').re_first(r'.*(\d{4}[-\/]\d{2}[-\/]\d{2})')
        try:
            house['apartment'] = house['title'].split(' ')[1]
        except Exception:
            pass
        house['city'] = response.css('div.crumbar a')[0].css('::text').re_first(r'(.*)公寓')
        house['district'] = response.css('div.crumbar a')[1].css('::text').re_first(r'(.*)公寓')
        house['block'] = response.css('div.crumbar a')[2].css('::text').re_first(r'(.*)公寓')

        rent_type = response.css("ul.house-info-list li")[1].re_first(
            REG['rent_type'])
        house['rent_type'] = v2k('rent_type', rent_type)
        house['features'] = response.css('ul.tags-list li.tag::text').extract()
        house['rental'] = int(response.css('div.detail_header span.price::text').extract_first())

        area = int(response.css("ul.house-info-list li")[0].re_first(REG['number']))
        house['room_area'] = area
        if rent_type == '整租':
            house['house_area'] = area
        huxing = response.css("ul.house-info-list li")[1].css('span').re(REG['huxing'])
        try:
            house['room_num'] = int(huxing[0])
            house['hall_num'] = int(huxing[1])
            house['bathroom_num'] = int(huxing[2])
        except Exception:
            pass
        house['orientation'] = response.css("ul.house-info-list li")[1].css('span').css('::text').re_first(
            r'.*?\s+(.*?)\s+')
        house['floor'], house['building_floor'] = response.css("ul.house-info-list li")[2].css('span').css('::text').re(
            r'(\d+)\/(\d+)')

        house['address'] = response.css("ul.house-info-list li")[3].css('span').css('::text').extract_first()

        try:
            house['traffic'] = response.css("ul.house-info-list li")[4].css('span').css('::text').extract_first()
        except Exception:
            pass

        house['content'] = trim(response.css("div.desc-wrap p#desc::text").extract_first())
        house['private_falicities'] = response.css("div.house-setup li::text").re(REG['configure'])

        # pictures
        house['pictures'] = response.css("ul#title-img-list img::attr(src)").re(REG['rm_url_params'])
        # longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])
        house['position'] = {
            'type': 'Point',
            'coordinates': [float(house['longi']), float(house['lati'])]
        }
        house['uniqe_key'] = uniqe_key(house)
        house['house_key'] = house_key(house)
        house['source_url'] = response.url
