# -*- coding: utf-8 -*-
import scrapy
from skywalk.items import *
from skywalk.utils import *
from skywalk.dict import *

REG = {
    'number': r'(\d+)',
    'yuan': r'(\d+)元',
    'huxing': r'(\d)室(\d)厅(\d)卫',
    'floor': r'(\d+)层.*?(\d+)层',
    'rent_type': r'(.租).*(.+?卧)',
    'payment': r'付(.)押(.)',
    'district_block': r'(.+?)\s+\-\s+(.+)',
    'longi': r'.*____json4fe\.lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati': r'.*____json4fe\.lat\s?=\s?\'(-?\d+\.\d+)\';',
    'city': r'.*var\s+city_name\s?=\s?\'(.*)\';',
    'price': r'(\d+).*?(\d+)',
    'configure': r'[^\r\n\s]+',
}


class Pinpai58Spider(scrapy.Spider):
    name = 'pinpai58'
    allowed_domains = ['58.com']
    start_urls = []
    custom_settings = {
        'CLOSESPIDER_ERRORCOUNT': 20,
        'DOWNLOAD_DELAY': 1.26,
        'CONCURRENT_REQUESTS': 8,
    }
    total_page = 100

    def start_requests(self):
        for i in range(200, 300):
            yield scrapy.Request('http://sh.58.com/pinpaigongyu/pn/' + str(i) + '/', self.parse)

    def parse_(self, response):
        '''
        解析列表分页
        '''
        # for link in response.css("div.page-numble a.num-unit::attr(href)").extract_first():
        # link =  response.css("div.page-numble a.num-unit::attr(href)").extract_first()
        # print(link)
        # # if link:
        # yield response.follow(self.start_urls[0],self.parse_page_url)
        return self.parse_page_url(response)

    def parse(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("ul.list li a::attr(href)").extract():
            yield response.follow(page_link, self.parse_page)

    def parse_page(self, response):
        '''
        解析内容
        '''
        print(response.url)
        house = HouseItem()
        # base info
        house['source_from'] = self.name

        # 通过字段判断，该房源是集中式公寓品牌页面还是普通页面
        special_title = response.css('p.head-title::text').extract_first()
        if special_title:
            return self.parse_spacial_page(response, house)
        else:
            return self.parse_normal_page(response, house)
        yield house

    def parse_spacial_page(self, response, house):
        house['title'] = response.css('p.head-title::text').extract_first()
        house['brand'] = house['title']
        house['rent_type'] = 3  # 公寓
        house['branch'] = response.css('p.head-address::text').extract_first()
        house['style'] = response.css('div.house-title div.housedetail span.bt::text').extract_first()
        house['empty_house_num'] = response.css('div.house-title div.housedetail span.houseNum::text').re_first(
            REG['number'])
        house['features'] = response.css('ul.tags-list li.tag::text').extract()
        house['rental'], house['rental_limit'] = response.css('div.detailMoney span.price::text').re(REG['price'])

        payment_rental, payment_deposit = response.css('div.detailMoney span.deposit::text').re(REG['payment'])
        house['payment_rental'], house['payment_deposit'] = chinese_to_arabic(payment_rental), chinese_to_arabic(
            payment_deposit)
        house['room_num'], house['hall_num'], house['bathroom_num'] = response.css("div.detailHX span::text").re(
            REG['huxing'])
        house['room_area'] = response.css("div.detailArea span::text").re(REG['number'])
        house['orientation'] = response.css("div.detailCX span::text").extract_first()
        house['address'] = response.css("div.detailAdress span::text").extract_first()

        house['content'] = response.css("div.describe-descri p.desc::text").extract_first()
        house['private_falicities'] = response.css("div.house-configure li::text").re(REG['configure'])

        # longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])
        yield house
