# coding:utf-8
import hashlib
from skywalk.settings import CITYS, DUPS_KEYS, HOUSE_KEYS
import time
import requests

"""
巴乐兔，字符串处理，解析数据
"""
REG = {
    'number': r'(\d+)',
    'yuan': r'(\d+)元',
    'huxing': r'(\d)室(\d)厅(\d)卫',
    'floor': r'(\d+)层.*(\d+)层',
    'rent_type': r'(.+?租).*(.+?卧)',
    'payment': r'付(.)押(.)',
    'district_block': r'(.+?)\s+\-\s+(.+)',
    'longi': r'.*var\s+s_lon\s?=\s?\'(-?\d+\.\d+)\';',
    'lati': r'.*var\s+s_lat\s?=\s?\'(-?\d+\.\d+)\';',
}


def trim(string):
    """
    remove \n,space
    """
    string = string.replace("\n", '').replace(' ', '').replace("\r", '')
    return string


def md5(str):
    """
    只适用utf-8编码
    """
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()


def create_uniqe_key(item, addition_values=[]):
    """
    生成唯一key
    :param item:
    :param addition_values:
    :return:
    """
    keys = DUPS_KEYS
    tokens = [str(item.get(k, '')) for k in keys]
    tokens.extend(addition_values)
    item_values_str = ''.join(tokens)
    """生成唯一键值"""
    return md5(item_values_str)


def uniqe_key(item):
    """
    生成唯一key
    :param item:
    :param addition_values:
    :return:
    """
    keys = DUPS_KEYS
    month_token = time.strftime("%Y-", time.localtime()) + str(hash_month(time.strftime("%m", time.localtime())))
    tokens = [str(item.get(k, '')) for k in keys]
    tokens.append(month_token)
    item_values_str = ''.join(tokens)
    """生成唯一键值"""
    return md5(item_values_str)


def house_key(item):
    """
    生成唯一key
    :param item:
    :param addition_values:
    :return:
    """
    keys = HOUSE_KEYS
    tokens = [str(item.get(k, '')) for k in keys]
    item_values_str = ''.join(tokens)
    """生成唯一键值"""
    return md5(item_values_str)


def hash_month(month):
    """
    根据月份生成hash月份值
    :param item:
    :return:
    """
    return int((int(month) - 1) / 3) * 3 + 1


def get_collection_name(city):
    """
    根据城市名获取mongodb的collection name，不存在则返回nocity
    """
    for key, value in CITYS.items():
        if value == city or value == '%s市' % (city,):
            return key
    return 'nocity'


def find_bathroom(str):
    str.find()

import random

KEYS = [
    "85052c21e2b9d408c249da5fc0c8a9fa",
    "5a1964338b3c14b25e09dcbab08e5892",
    "1a2da678b5c31959901e8d3f13fd64eb",
    "47865bbc4138cabdcb0e9f6ffd1f983b",
    "848a0721a4da7608d0302776a74005af",
    "68e66d66df3ed63f98f2e3ed46baca6a",
    "19b441ea42775e97a693bd7f5afbc6f8",
    "c38afce089a55f3fc25110e6eabbf079",
    # "4fffb787179883e0bbd61a22892316ac",
]
def get_subway(longi, lati, radius=3000):
    location = str(longi) + ',' + str(lati)
    url = 'http://restapi.amap.com/v3/place/around?key=%s&location=%s&output=json&radius=%s&types=地铁' % (random.choice(KEYS), location, radius)
    resp = requests.get(url)
    return [{'station': sub['name'], 'address': sub['address'], 'distance': int(sub['distance']), 'position': {
            'type': 'Point',
            'coordinates': [float(i) for i in sub['location'].split(',')]
        }} for sub in resp.json()['pois']]

def get_bus(longi, lati, radius=1500):
    location = str(longi) + ',' + str(lati)
    url = 'http://restapi.amap.com/v3/place/around?key=%s&location=%s&output=json&radius=%s&types=公交' % (random.choice(KEYS), location, radius)
    resp = requests.get(url)
    return [{'station': sub['name'], 'address': sub['address'], 'position': {
            'type': 'Point',
            'coordinates': [float(i) for i in sub['location'].split(',')]
        }} for sub in resp.json()['pois']]