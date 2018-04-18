# coding:utf-8
import re

'''
字符串处理，解析数据
'''

def trim(string):
    '''
    remove \n,space
    ''' 
    string = string.replace("\n", '').replace(' ','')
    return string