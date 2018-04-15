#coding:utf-8
#

DICT = {
	'baletu':{
		'config':{
			'衣柜':'衣橱',
			'沙发':'沙发',
			'电视':'电视',
			'冰箱':'冰箱',
			'空调':'空调',
			'热水器':'热水器',
			'无线网络':'无线网络',
			'微波炉':'微波炉',
			'厨房':'厨房',
			'卫生间':'卫生间',
		}
	}
}

FIELD_DICT = {
	'rent_type':{
		1:'整租',
		2:'合租',
		3:'公寓'
	},
	'bedroom_type':{
		1:'整租',
		2:'合租'
	}
}

CN_NUM = {
    '〇' : 0, '一' : 1, '二' : 2, '三' : 3, '四' : 4, '五' : 5, '六' : 6, '七' : 7, '八' : 8, '九' : 9, '零' : 0,
    '壹' : 1, '贰' : 2, '叁' : 3, '肆' : 4, '伍' : 5, '陆' : 6, '柒' : 7, '捌' : 8, '玖' : 9, '貮' : 2, '两' : 2,
}

CN_UNIT = {
    '十' : 10,
    '拾' : 10,
    '百' : 100,
    '佰' : 100,
    '千' : 1000,
    '仟' : 1000,
    '万' : 10000,
    '萬' : 10000,
    '亿' : 100000000,
    '億' : 100000000,
    '兆' : 1000000000000,
}

def v2k(hash_name,v):
	'''
	value转key
	'''
	hash = FIELD_DICT[hash_name]
	for key,value in hash.items():
		if value == v:
			return key
	return 0

def k2v(hash_name,k):
	'''
	key转value
	'''
	hash = FIELD_DICT[hash_name]
	return hash.get(k,0)

def dv2k(dict_name,hash_name,v):
	'''
	value转key
	'''
	hash = DICT[dict_name][hash_name]
	for key,value in hash.items():
		if value == v:
			return key
	return v

def dk2v(dict_name,hash_name,k):
	'''
	key转value
	'''
	hash = DICT[dict_name][hash_name]
	return hash.get(k,k)

def chinese_to_arabic(cn:str) -> int:
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val