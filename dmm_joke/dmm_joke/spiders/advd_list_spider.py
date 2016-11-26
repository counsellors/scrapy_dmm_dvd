# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from scrapy.selector import Selector
from dmm_joke.items import ADVDDetailListItem
from scrapy.spiders import  CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class AdvdListSpiderSpider(scrapy.Spider):
    name = "advd_list_spider"
    allowed_domains = ["dmm.co.jp"]
    start_urls = ['http://www.dmm.co.jp/digital/videoa/-/genre/']
    start_urls = ["file:///tmp/detail_list.html"]
    # 再一次爬去中, scrapy在rule中是自动去重的,额，省了很多事
    # Rule(LinkExtractor(allow=('/rental/\-/list/=/.*page', ))),
    # rules = (
    #     Rule(LinkExtractor(allow=('/rental/\-/list/=/.*page=3', ))),
    #     Rule(LinkExtractor(allow=('/rental/\-/detail/=/cid=\w+/', )), callback='parse_item'),

    # )

    def get_fields(self, sel,item):
        items = []
        for m_field in sel:
            d_item = {}
            d_item['link'] = m_field.xpath("div/p[2]/a/@href").extract()[0]
            d_item['img_url'] = m_field.xpath("div/p[2]/a/span[1]/img/@src").extract()[0]
            d_item['img_desc'] = m_field.xpath("div/p[2]/a/span[1]/img/@alt").extract()[0]
            d_item['price'] = m_field.xpath("div/div/p[1]/text()").extract()[0]
            items.append(d_item)
        return items

    def parse(self, response):
        sel = Selector(response)
        items = []
        sel_list = sel.xpath("//*[@id='list']/li")
        for m_field in sel_list:
            d_item = ADVDDetailListItem()
            d_item['m_type'] = 'advd_list'
            print m_field.extract()
            d_item['link'] = m_field.xpath("div/p[@class='tmb']/a/@href").extract()[0]
            d_item['img_url'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@src").extract()[0]
            d_item['img_desc'] = m_field.xpath("div/p[@class='tmb']/a/span[1]/img/@alt").extract()[0]
            d_item['price'] = m_field.xpath("div/div/p[1]/text()").extract()[0]
            items.append(d_item)
        return items
