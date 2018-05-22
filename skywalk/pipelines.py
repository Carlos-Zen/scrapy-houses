# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from pymongo.errors import *
from skywalk.items import INT_FIELD
from skywalk.utils import get_subway, get_bus

# class SkywalkPipeline(object):
#     def process_item(self, item, spider):
#         print(item)
#         return item


# class DupsPipeline(object):
#
#     collection_name = 'house_shanghai'
#     count = 0
#     def __init__(self, mongo_uri, mongo_db,crawler):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#         self.crawler = crawler
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE', 'house'),
#             crawler=crawler
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         # self.db[self.collection_name].insert(dict(item))
#         self.count += 1
#         print(self.count)
#         if self.count == 3:
#             self.crawler.engine.close_spider(spider, 'No new record condition matched.')
#         return item

class MongoPipeline(object):
    collision_collection = ''
    collection_name = ''
    dups_count = 0

    def __init__(self, crawler):
        self.crawler = crawler
        self.mongo_uri = crawler.settings.get('MONGO_URI')
        self.mongo_db = crawler.settings.get('MONGO_DATABASE', 'house')
        self.mongo_db_collision = crawler.settings.get('MONGO_DATABASE_COLLISION', 'house_collision')

        self.collection_name = crawler.settings.get('MONGO_COLLECTION_PRE', 'house_%s')
        self.collision_collection = crawler.settings.get('MONGO_COLLECTION_COLLISION', 'collision')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler=crawler
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db_collision = self.client[self.mongo_db_collision]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        插入对应collection，并处理重复数据。重复过多则结束该spider
        :param item:
        :param spider:
        :return:
        """
        # int转化部分参数
        [item.set(f, int(item.get(f, 0))) for f in INT_FIELD]

        if item['district'][-1] not in ['区', '县']:
            item['district'] = item['district'] + '区'

        # 加入地铁数据

        try:
            item['subway'] = get_subway(item['longi'], item['lati'])
            # item['bus'] = get_bus(item['longi'], item['lati'])
        except Exception:
            pass
        # 重复数据导致spider中断
        if self.crawler.settings.get('DUPS_STOP') and self.dups_count == self.crawler.settings.get('DUPS_LIMIT'):
            self.crawler.engine.close_spider(spider, 'Dups item reach the limit .')

        collection_name = self.collection_name % (item['collection'],)

        try:
            self.db[collection_name].insert(dict(item))
        except DuplicateKeyError:
            # 重复计数，插入重复库中
            self.dups_count += 1
            # self.db_collision[self.collision_collection].insert(dict(item))
        return item
