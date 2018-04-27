#coding:utf-8
#
from pymongo.errors import *
import pymongo
from bson.objectid import ObjectId
from skywalk.utils import *
from skywalk.settings import *
import datetime
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
    for d in collection.find({},no_cursor_timeout=True):
        # print(d)
        uk = uniqe_key(d)
        nuk = create_uniqe_key(d)
        hk = house_key(d)
        # print(uk, ukn)
        upi = update_int(d)
        up = {'house_key': hk, 'uniqe_key': uk,'uniqe_key_no_date': nuk}
        up.update(upi)
        try:
            collection.update_one({'_id': ObjectId(d['_id'])}, {'$set': up}, upsert=True)
        except DuplicateKeyError:
            collection.remove({'_id':d['_id']})
    client.close()
        # break

def update_int(item):
    update = {}
    for key in ['floor','building_floor','rental','rental_limit','service_fee','deposit','payment_deposit','payment_rental','room_area','house_area']:
        update[key] = item.get(key,0)
    return update

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

def update_collections_uniqe_keys():

    for col in collections:
        update_unique_key('house',col)


def count_house_record():
    total = 0
    count_collection = client['log']['count']
    for col in collections:
        collection = client['house'][col]
        count = collection.count()
        print(count)
        total = total+count
        count_collection.insert({'date': datetime.datetime.now(), 'count': count, 'city': col[6:]})
    count_collection.insert({'date': datetime.datetime.now(), 'count': total, 'city': 'all_cities'})