# coding:utf-8
import re

'''
巴乐兔，字符串处理，解析数据
'''
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