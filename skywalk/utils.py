# coding:utf-8
import hashlib
from skywalk.settings import CITYS, DUPS_KEYS

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
    tokens = [str(item.get(k,'')) for k in keys]
    tokens.extend(addition_values)
    item_values_str = ''.join(tokens)
    """生成唯一键值"""
    return md5(item_values_str)


def get_collection_name(city):
    """
    根据城市名获取mongodb的collection name，不存在则返回nocity
    """
    for key, value in CITYS.items():
        if value == city or value == '%s市' % (city,):
            return key
    return 'nocity'

def get_collection_name(city):
    """
    根据城市名获取mongodb的collection name，不存在则返回nocity
    """
    for key, value in CITYS.items():
        if value == city or value == '%s市' % (city,):
            return key
    return 'nocity'
