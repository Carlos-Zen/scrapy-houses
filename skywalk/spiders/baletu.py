# -*- coding: utf-8 -*-
import scrapy
from skywalk.items import *
from skywalk.spider.utils import *

REG = {
    'number':r'(\d+)',
    'yuan':r'(\d+)元',
    'huxing':r'(\d)室(\d)厅(\d)卫',
    'floor':r'(\d+)层.*(\d+)层',
    'rent_type':r'(.+?租).*(.+?卧)',
    'payment':r'付(.)押(.)',
    'district_block':r'(.+?)\s+\-\s+(.+)',
    'longi':r'.*var\s+s_lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati':r'.*var\s+s_lat\s?=\s?\'(-?\d+\.\d+)\';',
}

def trim(string):
    '''
    remove \n,space
    ''' 
    string = string.replace("\n", '').replace(' ','')
    return string

class BaletuSpider(scrapy.Spider):
    name = 'baletu'
    allowed_domains = ['baletu.com']
    start_urls = ['http://sh.baletu.com/zhaofang/']

    def parse(self, response):
        '''
        解析列表分页
        '''
        for link in response.css("div.page-numble a.num-unit::attr('href')"):
            yield response.follow(link,self.parse_page_url)

    def parse_page_url(self, response):
        '''
        解析内容页链接
        '''
        for page_link in response.css("li.PBA_list_house a::attr('href')"):
            yield response.follow(page_link,self.parse_page)

    def parse_page(self, response):
        '''
        解析内容
        ''' 
        house = HouseItem()
        house['title'] = response.css("div.basic-title a::text").extract_first()
        house['apartment'] = house['title']
        house['rental'] = response.css("div.house-text-Akey li.price::text").re_first(REG['yuan'])
        house['room_area'] = response.css("div.house-text-Akey li.cent::text").re_first(REG['number'])
        house['orientation'] = response.css("div.house-text-Akey li::text")[2].extract_first()
        house['city'] = trim(response.css("div.region a")[2].extract_first())

        house['trafic'] = response.css("div.house-text-list dd::text")[0].extract_first()
        house['room_num'],house['hall_num'],house['bathroom_num'] = response.css("div.house-text-list dd::text")[1].re(REG['huxing'])
        house['floor'],house['building_floor'] = response.css("div.house-text-list dd::text")[2].re(REG['floor'])
        payment_rental,payment_deposit = response.css("div.house-text-list dd::text")[3].re(REG['rent_type'])
        house['floor'],house['building_floor'] = v2k('rent_type',rent_type),v2k('bedroom_type',bedroom_type)

        house['floor'] = response.css("div.house-text-list dd::text")[0].extract_first()
        house['room_num'] = response.css("div.house-text-list dd::text")[0].extract_first()
        house['room_num'] = response.css("div.house-text-list dd::text")[0].extract_first()