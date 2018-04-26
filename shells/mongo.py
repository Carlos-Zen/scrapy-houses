#coding:utf-8
#

import pymongo
from bson.objectid import ObjectId
from skywalk.utils import *
# async def log(message):
client = pymongo.MongoClient('mongodb://10.6.52.147:27017')
collections = [
        "house_beijing",
        "house_chengdu",
        "house_chongqing",
        "house_guangzhou",
        "house_hangzhou",
        "house_nanjing",
        "house_shanghai",
        "house_suzhou",
        "house_tianjin",
        "house_wuhan",
        "house_xian",
        "house_zhengzhou"
    ]

def update_unique_key(db,col):
    collection = client[db][col]
    for d in collection.find({}):
        # print(d)
        uk = uniqe_key(d)
        hk = house_key(d)
        # print(uk, ukn)
        collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': {'house_key': hk, 'uniqe_key': uk}}, upsert=True)
        # break

def delete_dups_row(db,col):
    collection = client[db][col]
    keys = {}
    for k in collection.find({}):
        key = k['uniqe_key']
        if key in keys:
            print('duplicate key %s' % key)
            collection.remove({'_id': k['_id']})
        else:
            print('first record key %s' % key)
            keys[key] = 1

def test_insert_dups(db,col):
    items = {'uniqe_key':'629da19c051e9d2f0ef6a22eefa9d15e'}
    collection = client[db][col]
    collection.insert(items)

def update_position_key(db,col):
    collection = client[db][col]
    for d in collection.find({}):
        # print(d)
        position = {
            'type':'Point',
            'coordinates': [float(d['longi']),float(d['lati'])]
        }
        # print(uk, ukn)
        collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': {'position': position}}, upsert=True)

def delete_collections_dups_keys():
    for col in collections:
        delete_dups_row('house',col)

def update_collections_posotion():

    for col in collections:
        update_position_key('house',col)