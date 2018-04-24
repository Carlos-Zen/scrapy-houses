# -*- coding: utf-8 -*-
from shells import mongo

# mongo.delete_dups_row('house', 'house_shanghai')
# mongo.test_insert_dups('house', 'house_shanghai')

# mongo.update_collections_posotion()
# mongo.delete_collections_dups_keys()

from bson.json_util import dumps


te = "{'address': '三间房南里七号院', 'bathroom_num': '1', 'block': '双桥', 'brand': '乐乎公寓', 'building_floor': '5', 'city': '北京', 'collection': 'beijing', 'content': '\r\n''【乐乎品牌公寓】乐乎城市青年社区！ ''打造80、90现代社区，我们社区不定期的社区活动与您身边的乐友一起互动，让您在北漂的生活中一个温暖的家；我们住的不只是房子，而是另一种生活交通便利：地铁双桥站，步行8分钟即到。公交：312路、342路、397路、411路、475路、506路、摆站506路、等直达大望路国贸四惠生活购物：附近有永辉超市，国泰百货，世纪华联等大型超市；还有农贸市场等。满足日常生活所需。房间配置: ''独门独户，有独立卫生间，开放式厨房，精装修，全新品牌家电，公区高速WiFi覆盖，智能*门锁，集体供暖。公寓配套服务：1.免费健身房，咖啡厅，丰富您的业余时间2.每月1次免费入室清洁服务；3.网上、电话均可报修，免费上门维修4.代收代发快>递；5.社区24小时无缝*，保安定时巡逻；6.定期举办社区活动，住户都可以免费参加，喜欢交朋友的住户的福利哦！!!!!!7.免费停车场，给你的爱车找一个家，告别停车烦恼！付款方式：押一付一，押一付三都可以；有意向的请联系我！全北京32家连锁店,欢迎来电>咨询!', 'crawl_date': '2018-04-24', 'district': '朝阳', 'features': ['离地铁近', '独立卫生间', '厨房'], 'floor': '3', 'hall_num': '1', 'house_area': '20', 'lati': '39.910139', 'longi': '116.576709', 'orientation': '朝南', 'pictures': ['//pic1.58cdn.com.cn/gongyu/n_v2b4de76b82e314c348e8627e42b57e8cd_017b3613deda4301.jpg','//pic1.58cdn.com.cn/gongyu/n_v20de09fc660f64d18bc58f0a3d93b27ec_908f066a5d6dcd33.jpg','//pic1.58cdn.com.cn/gongyu/n_v2f17d4725e52d427eb682b9ae13381647_afa20817c5c8ade7.jpg','//pic1.58cdn.com.cn/gongyu/n_v2053aa7bcc63a4656a38707b828e82e06_6124b2330810072f.jpg'], 'position': ['116.576709', '39.910139'], 'private_falicities': ['床','衣柜','书桌','空调','餐桌','暖气','电视机','热水器','洗衣机','冰箱','WIFI','沙发','橱柜','油烟机'], 'publish_date': '2018-04-20', 'rent_type': 1, 'rental': '2650', 'room_area': '20', 'room_num': '1', 'source_from': 'pinpai58', 'title': '【整租】双桥 乐乎城市青年社区 1室1厅', 'uniqe_key': '40cb9b6ab760b9f5186bfa5edc2317ed', 'uniqe_key_no_date': '31c20fb4c663037d82f794d4c1220b21'}"
te = {'address': '沙阳路34号',
 'bathroom_num': '1',
 'block': '沙河',
 'brand': '宝铂公寓',
 'building_floor': '18',
 'city': '北京',
 'collection': 'beijing',
 'content': "购物方便：小区周围有、大型商场、大型超市、菜市场、饭店、医院、KTV、修车、洗车、美容美发、还有五湖四海的小吃，让您在自己家门口就能吃到五湖四海的美味！好房不等人，如果您看到了希望马上联系我！附近有多次公交线路,专50公交直通小>区，小区南门有菜市场，小区内环境特别好，周围各种饭店生活商店，家具齐全，精装修（图片为真实图片），看上的抓紧联系我吧！！！                    ",
 'crawl_date': '2018-04-24',
 'district': '昌平',
 'features': ['离地铁近', '独立阳台', '独立卫生间', '厨房'],
 'floor': '7',
 'hall_num': '1',
 'house_area': '50',
 'lati': '40.124517',
 'longi': '116.274683',
 'orientation': '朝南',
 'pictures': ['//pic1.58cdn.com.cn/gongyu/n_v2685bcfb450f34dcca167f739c81b1a53_2382c4a4751a7b4f.jpg',
              '//pic1.58cdn.com.cn/gongyu/n_v27d0657042f5848f59be48998a8fd1f59_195fcb46b8c9e631.jpg',
              '//pic1.58cdn.com.cn/gongyu/n_v2fcfa745b10e149fd8efe23ace583f393_31e5b9611d597820.jpg',
              '//pic1.58cdn.com.cn/gongyu/n_v277c793f40dc144528280902792c42786_21ea0bed573dbd52.jpg'],
 'position': ['116.274683', '40.124517'],
 'private_falicities': ['床',
                        '衣柜',
                        '书桌',
                        '空调',
                        '餐桌',
                        '暖气',
                        '电视机',
                        '燃气',
                        '热水器',
                        '洗衣机',
                        '冰箱',
                        'WIFI',
                        '沙发',
                        '橱柜',
                        '油烟机'],
 'publish_date': '2018-04-23',
 'rent_type': 1,
 'rental': '3000',
 'room_area': '50',
 'room_num': '1',
 'source_from': 'pinpai58',
 'title': '【整租】沙河 保利罗兰香谷 1室1厅',
 'traffic': '距离昌平线巩华城站2.6km',
 'uniqe_key': 'ffdc5f9680fa49fe7246d605b8735673',
 'uniqe_key_no_date': 'd9d1007b0690fdfe241ffaa6a5736e28'}

# te.encode('utf-8')
dumps(te)