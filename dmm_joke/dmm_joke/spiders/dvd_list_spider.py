# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from scrapy.selector import Selector
from dmm_joke.items import DVDDetailListItem
from scrapy.spiders import  CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class DvdListSpiderSpider(CrawlSpider):
    name = "dvd_list_spider"
    allowed_domains = ["dmm.com"]
    start_urls = ['http://www.dmm.com/rental/ppr/-/list/=/article=category/id=japanese/limit=120/sort=date/page=2']
    # start_urls = ["file:///tmp/dvd_genre.html"]
    rules = (
        Rule(LinkExtractor(allow=('rental/ppr/-/list/=/article=category/id=japanese/', ),
            deny =('limit=30','limit=60','view=text',) 
            ), callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        items = []
        sel_list = sel.xpath("//*[@id='list']/li")
        for m_field in sel_list:
            d_item = DVDDetailListItem()
            d_item['m_type'] = 'dvd_list'
            d_item['link'] = m_field.xpath("div/p[@class='tmb']/a/@href").extract()[0]
            d_item['img_url'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@src").extract()[0]
            d_item['img_desc'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@alt").extract()[0]
            d_item['price'] = m_field.xpath("div/div/p[1]/text()").extract()[0]
            items.append(d_item)
        return items
