# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
import datetime


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = client.get_database(settings['MONGODB_DB'])
        self.collections = {}
        for table_name in settings['MONGODB_COLLECTION']:
            logging.log(logging.INFO, 'Init MongoDB Table: {0}'.format(table_name))
            self.collections[table_name] = db.get_collection(table_name)

    def process_item(self, item, spider):
        now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing {0}'.format(data))
        if item.get('m_type') is None:
            raise DropItem('Missing item {0} type for mongodb'.format(item['link']))
        if valid:
            if (self.collections[item['m_type']].find({"link":item['link']}).count() ==0):
                item['create_time'] = now_time
                item['update_time'] = now_time
            else:
                item['update_time'] = now_time
            self.collections[item['m_type']].update({'link': item['link']},
                                   dict(item), upsert=True)
            logging.log(logging.INFO, 'Movie added to MongoDB database!')

        return item

class DmmJokePipeline(object):
    def process_item(self, item, spider):
        return item
