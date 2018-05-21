# coding:utf-8

import pymongo
from bson.objectid import ObjectId
import datetime
from multiprocessing import Pool
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


# def update_data(db,col):
#     collection = client[db][col]
#     for d in collection.find(no_cursor_timeout=True):
#         up = dict()
#         try:
#             if d['district'][-1] not in ['区','县']:
#                 up['district'] = d['district']+'区'
#                 collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': up})
#         except Exception:
#             print(up)
#             pass
#     client.close()

def update_data(db,col):
    collection = client[db][col]
    for d in collection.find(no_cursor_timeout=True):
        up = dict()
        try:
            if d['brand'] == 'ziroom':
                up['brand'] = '自如友家'
            up['subway'] = get_subway(d['longi'], d['lati'])
            up['bus'] = get_bus(d['longi'], d['lati'])
            collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': up}, upsert=True)
        except Exception:
            print(up)
            pass
    client.close()


def update_collections_uniqe_keys():
    p = Pool(len(collections))
    for col in collections:
        p.apply(update_data, ('house', col))
    p.close()
    p.join()

# update_collections_uniqe_keys()
# update_data('house','house_chengdu')