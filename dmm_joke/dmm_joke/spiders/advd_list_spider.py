# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from scrapy.selector import Selector
from dmm_joke.items import ADVDDetailListItem
from scrapy.spiders import  CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

class AdvdListSpiderSpider(RedisCrawlSpider):
    name = "advd_list_spider"
    redis_key = 'advd_list_spider:start_urls'
    allowed_domains = ["dmm.com"]
    # start_urls = ["file:///tmp/detail_list.html"]
    start_urls = ["file:///tmp/advd_genre.html"]
    rules = (

        Rule(LinkExtractor(allow=('digital/videoa/\-/list/=/article=keyword/id', ),
            deny =('sort=','limit=30','limit=60','view=text',) 
            ), callback='parse_item'),

    )

    def parse_item(self, response):
        sel = Selector(response)
        items = []
        print "lalla",response
        sel_list = sel.xpath("//*[@id='list']/li")
        for m_field in sel_list:
            print "extract field.."
            d_item = ADVDDetailListItem()
            d_item['m_type'] = 'advd_list'
            print m_field.extract()
            d_item['link'] = m_field.xpath("div/p[@class='tmb']/a/@href").extract()[0]
            d_item['img_url'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@src").extract()[0]
            d_item['img_desc'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@alt").extract()[0]
            d_item['price'] = m_field.xpath("div/div/p[1]/text()").extract()[0]
            items.append(d_item)
        return items
