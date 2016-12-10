# -*- coding: utf-8 -*-

import os,sys
import pymongo
import redis 
from scrapy.conf import settings

def loadurls(table_name, start_urls):
    r = redis.Redis(host='localhost',port=6379,db=0)
    client = pymongo.MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
        )
    db = client.get_database(settings['MONGODB_DB'])
    m_collection = db.get_collection(table_name)
    cursor = m_collection.find()
    for document  in cursor:
        hostname = "http://www.dmm.com"
        item_url =  hostname+document['link']
        r.lpush(start_urls, item_url)
        print document['img_desc'].encode('utf8')
        print item_url
    print r.llen(start_urls)

def main():
    table_name = 'dvd_list_copy'
    start_urls = 'dvd_spider:start_urls'
    loadurls(table_name, start_urls )

if __name__ == '__main__':
    main()