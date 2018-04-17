# -*- coding: utf-8 -*-
import scrapy
from skywalk.items import *
from skywalk.utils import *
from skywalk.dict import *

REG = {
    'number':r'(\d+)',
    'yuan':r'(\d+)元',
    'huxing':r'(\d)室(\d)厅(\d)卫',
    'floor':r'(\d+)层.*?(\d+)层',
    'rent_type':r'(.租).*(.+?卧)',
    'payment':r'付(.)押(.)',
    'district_block':r'(.+?)\s+\-\s+(.+)',
    'longi':r'.*var\s+s_lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati':r'.*var\s+s_lat\s?=\s?\'(-?\d+\.\d+)\';',
    'city':r'.*var\s+city_name\s?=\s?\'(.*)\';',
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

    def start_requests(self):
        for i in range(200,300):
            yield scrapy.Request('http://sh.baletu.com/zhaofang/p'+str(i)+'/', self.parse)

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
        for page_link in response.css("li.PBA_list_house a::attr(href)").extract():
            yield response.follow(page_link,self.parse_page)

    def parse_page(self, response):
        '''
        解析内容
        ''' 
        print(response.url)
        house = HouseItem()
        house['title'] = response.css("div.basic-title a::text").extract_first()
        house['apartment'] = house['title']
        house['rental'] = response.css("div.house-text-Akey li.price::text").extract_first()
        house['room_area'] = response.css("div.house-text-Akey li.cent::text").extract_first()
        house['orientation'] = response.css("div.house-text-Akey li")[2].css("::text").extract_first()
        house['city'] = response.css('script').re_first(REG['city'])

        house['traffic'] = response.css("div.house-text-list dd::text").extract_first()
        house['room_num'],house['hall_num'],house['bathroom_num'] = response.css("div.house-text-list dd::text")[1].re(REG['huxing'])
        house['floor'],house['building_floor'] = response.css("div.house-text-list dd")[2].css("::text").re(REG['floor'])

        rent_type_string = trim(response.css("div.house-text-list dd")[3].css("::text").extract_first())
        if rent_type_string.find('-') != -1:
            rent_type,bedroom_type = response.css("div.house-text-list dd")[3].css("::text").re(REG['rent_type'])
            house['rent_type'],house['bedroom_type'] = v2k('rent_type',trim(rent_type)),v2k('bedroom_type',bedroom_type)
        else:
            house['rent_type'] = v2k('rent_type',trim(rent_type_string))

        payment_rental,payment_deposit = response.css("div.house-text-list dd")[4].css("::text").re(REG['payment'])
        house['payment_rental'],house['payment_deposit'] = chinese_to_arabic(payment_rental),chinese_to_arabic(payment_deposit)

        house['district'],house['block'] = response.css("div.house-text-list dd")[5].css('a::text').extract()
        house['address'] = response.css("div.house-text-list dd")[6].css('::text').extract_first()

        #pictures
        house['pictures'] = response.css('div.imagesPreviewer .i-images img::attr(data-src)').extract()

        #longti,lati
        house['longi'] = response.css('script').re_first(REG['longi'])
        house['lati'] = response.css('script').re_first(REG['lati'])

        #falicities
        house['private_falicities'] = [dv2k('baletu','config',fal) for fal in response.css('div#privateFalicities li img::attr(alt)').extract()]
        house['public_falicities'] = [dv2k('baletu','config',fal) for fal in response.css('div#publicFalicities li img::attr(alt)').extract()]
        yield house