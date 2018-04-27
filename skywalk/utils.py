# coding:utf-8
import hashlib
from skywalk.settings import CITYS, DUPS_KEYS, HOUSE_KEYS
import time

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
