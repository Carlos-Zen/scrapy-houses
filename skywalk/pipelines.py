# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

class SkywalkPipeline(object):
    def process_item(self, item, spider):
        print(item)
        return item



class MongoPipeline(object):

    collection_name = 'house_shanghai'
    count = 0
    def __init__(self, mongo_uri, mongo_db,crawler):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'house'),
            crawler=crawler
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # self.db[self.collection_name].insert(dict(item))
        self.count += 1
        print(self.count)
        if self.count == 10:
            self.crawler.engine.close_spider(spider)
        return item