#coding:utf-8
#

import pymongo
from bson.objectid import ObjectId
from skywalk.utils import *
# async def log(message):
client = pymongo.MongoClient('mongodb://10.6.52.147:27017')


def update_unique_key():
    collection = client[db][col]
    for d in collection.find({}):
        # print(d)
        uk = create_uniqe_key(d, ['2018-04'])
        ukn = create_uniqe_key(d)
        # print(uk, ukn)
        collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': {'uniqe_key_no_date': ukn, 'uniqe_key': uk}}, upsert=True)
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
