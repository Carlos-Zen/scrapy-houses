# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):

    title = scrapy.Field()
    content = scrapy.Field()
    brand = scrapy.Field()
    province = scrapy.Field()
    city = scrapy.Field()
    district = scrapy.Field()
    block = scrapy.Field()
    address = scrapy.Field()
    lati = scrapy.Field()
    longi =scrapy.Field()
    apartment = scrapy.Field()
    rent_type = scrapy.Field() # scrapy.Field()整租/ 2合租/ 3公寓
    bedroom_type = scrapy.Field() # 主卧：scrapy.Field()，次卧：2
    room_num = scrapy.Field()
    hall_num = scrapy.Field()
    bathroom_num = scrapy.Field()
    floor = scrapy.Field()
    building_floor = scrapy.Field()
    rental = scrapy.Field()
    deposit = scrapy.Field()
    payment_deposit = scrapy.Field() #付款方式押金月份
    payment_rental = scrapy.Field() #付款方式租金月份
    orientation = scrapy.Field() #朝向
    deroration = scrapy.Field()
    room_area = scrapy.Field() #面积
    house_area = scrapy.Field()
    exclusive_bathroom = scrapy.Field()
    exclusive_balcony = scrapy.Field() 
    publish_date = scrapy.Field()
    pictures = scrapy.Field()
    source_from = scrapy.Field()
    publisher = scrapy.Field()
    traffic = scrapy.Field()
    uniqe_key = scrapy.Field()
    private_falicities = scrapy.Field()
    public_falicities = scrapy.Field()
