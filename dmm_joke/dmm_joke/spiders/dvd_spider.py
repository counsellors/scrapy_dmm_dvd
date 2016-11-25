# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector
from dmm_joke.items import DVDDetailItem
from scrapy.spiders import  CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class DvdSpiderSpider(CrawlSpider):
    name = "dvd_spider"
    allowed_domains = ["dmm.com"]
    start_url_template = 'http://www.dmm.com/rental/-/list/=/sort=ranking/page='
    start_urls = ["http://www.dmm.com/en/rental/-/list/=/article=maker/id=60011/limit=30/view=text/page=2/"]
    # start_urls = ["http://www.dmm.com/en/rental/-/detail/=/cid=n_611vwdg6298r/"]
    start_urls = ["file:///tmp/index.html"]
    # start_urls = ["file:///tmp/index.html.1"]
    # 再一次爬去中, scrapy在rule中是自动去重的,额，省了很多事
    # Rule(LinkExtractor(allow=('/rental/\-/list/=/.*page', ))),
    # rules = (
    #     Rule(LinkExtractor(allow=('/rental/\-/list/=/.*page=3', ))),
    #     Rule(LinkExtractor(allow=('/rental/\-/detail/=/cid=\w+/', )), callback='parse_item'),

    # )

    def get_item_list(self, sel, index, field_name, item):
        detail_xpath = "//div[@class='page-detail']/table/tr/td[1]/table/tr[%s]/td[2]/a"
        m_field_list = sel.xpath(detail_xpath%(index))
        item[field_name] = []
        for m_field in m_field_list:
            items = []
            items.append(m_field.xpath("text()").extract()[0])
            items.append(m_field.xpath("@href").extract()[0])
            item[field_name].append(items)

    def parse(self, response):
        sel = Selector(response)
        items = []
        item = DVDDetailItem()
        item['link'] = response.url
        item['img_url'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/div/div[@id='sample-video']/a/img/@src").extract()
        item['title'] = sel.xpath("//div[@class='page-detail']/div[@class='area-headline group']/div[@class='hreview']/h1/span/text()").extract()
        detail_xpath = "//div[@class='page-detail']/table/tr/td[1]/table/tr[%s]/td[2]/text()"
        for index in xrange( len(DVDDetailItem.m_fields) ):
            item[item.m_fields[index]] = sel.xpath(detail_xpath%(index)).extract()
        self.get_item_list(sel, 5, 'performers', item)
        self.get_item_list(sel, 6, 'supervision', item)
        self.get_item_list(sel, 7, 'production', item)
        self.get_item_list(sel, 14, 'studios', item)
        self.get_item_list(sel, 15, 'genre', item)
        item['slogan'] = sel.xpath("//div[@class='page-detail']/table[@class='mg-b12']/tr/td[1]/div[@class='clear tx14 lh4 bold']/text()").extract()
        item['brief'] = sel.xpath("//div[@class='page-detail']/table[@class='mg-b12']/tr/td[1]/div/p/text()").extract()
        # items.append(item)
        yield item