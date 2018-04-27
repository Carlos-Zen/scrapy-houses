# coding: utf-8

from skywalk.utils import *
from shells.mongo import update_int

house = {'apartment': '悦澜水岸家园',
 'block': '物资学院路',
 'brand': 'danke',
 'building_floor': 18,
 'city': '北京',
 'collection': 'beijing',
 'crawl_date': '2018-04-27',
 'deposit': 0,
 'district': '通州区',
 'exclusive_bathroom': 1,
 'features': ['独卫', '独立淋浴', '集中供暖'],
 'floor': 1,
 'hall_num': 1,
 'house_area': 0,
 'house_key': '94dc311e1f01a548d69305151530ffe3',
 'lati': '39.947596',
 'longi': '116.665902',
 'orientation': '南',
 'payment_deposit': 1,
 'payment_rental': 1,
 'pictures': ['https://public.wutongwan.org/public-20180425-FgdacUTXIP9QH2ApIrpJDe0lN-uD-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-FjTmTG_qFslkmOpUlHVv8vF-kVwe-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-FlVDjVL6bb3O4j7yQ8hhYIg_S2xY-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-FuE1ja30mD89skxDmmMzw-AMvk2U-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-Fr6L9mAznOMuVDx6Au89_DhGTVj9-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-FheeXy5-i-mB8vSub1aQj7gc6PtH-roomPcDetail.jpg',
              'https://public.wutongwan.org/public-20180425-Fig_ZmeNTQ3WK4egWk_Hm1ETK7r3-roomPcDetail.jpg'],
 'position': {'coordinates': [116.665902, 39.947596], 'type': 'Point'},
 'rent_type': 2,
 'rental': 2590,
 'rental_limit': 0,
 'room_area': 17,
 'room_num': 4,
 'service_fee': 2719,
 'source_from': 'danke',
 'title': '物资学院路悦澜水岸家园主卧朝南C室',
 'traffic': ['距6号线物资学院路站2350米'],
 'uniqe_key': '0c676d0e299e56f259b73aea6be7ff6a',
 'uniqe_key_no_date': '0c676d0e299e56f259b73aea6be7ff6a'}

# uniqe_key(house)
update_int(house)