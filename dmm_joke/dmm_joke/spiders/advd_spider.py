# -*- coding: utf-8 -*-
import scrapy
import os
import datetime
from scrapy.selector import Selector
from dmm_joke.items import ADVDDetailItem
from scrapy.spiders import  CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

class AdvdSpiderSpider(CrawlSpider):
    name = "advd_spider"
    allowed_domains = ["dmm.com"]
    start_urls = ['http://www.dmm.com/ppr']
    start_urls = ["file:///tmp/index3.html"]
    start_urls = ["file:///tmp/black1.html"]
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

    def get_img_list(self, sel, field_name, item):
        detail_xpath = "//*[@id='sample-image-block']/a"
        m_field_list = sel.xpath(detail_xpath)
        item[field_name] = []
        for m_field in m_field_list:
            items = []
            items.append(m_field.xpath("@id").extract()[0])
            items.append(m_field.xpath("img/@src").extract()[0])
            item[field_name].append(items)

    def parse(self, response):
        sel = Selector(response)
        items = []
        item = ADVDDetailItem()
        item['m_type'] = 'advd'
        item['link'] = response.url
        item['img_url'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/div/div[@id='sample-video']/a/img/@src").extract()
        item['title'] = sel.xpath("//div[@class='page-detail']/div[@class='area-headline group']/div[@class='hreview']/h1[@id='title']/text()").extract()
        item['platform'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[2]/td[2]/text()").extract()
        item['delivery_start_date'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/td[2]/text()").extract()
        item['release_date'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[3]/td[2]/text()").extract()
        item['recorded_time'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[4]/td[2]/text()").extract()
        item['series'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[7]/td[2]/text()").extract()
        item['movie_id'] = sel.xpath("//*[@id='mu']/div/table/tr/td[1]/table/tr[11]/td[2]/text()").extract()
        item['average_rating'] = sel.xpath("//*[@id='mu']/div/table/tr/td[1]/table/tr[12]/td[2]/img/@src").extract()
        item['brief'] = sel.xpath("//*[@id='mu']/div/table/tr/td[1]/div[4]/text()").extract()
        self.get_item_list(sel, 5, 'performers', item)
        self.get_item_list(sel, 6, 'supervision', item)
        self.get_item_list(sel, 8, 'studios', item)
        self.get_item_list(sel, 9, 'lables', item)
        self.get_item_list(sel, 10, 'genre', item)
        self.get_img_list(sel, 'sample_images', item)
        item['total_comment_num'] = 0
        if not item['average_rating'][0].endswith("0.gif"):
            item['total_comment_num'] = int(response.xpath("//*[@id='review']/div[2]/div/div[1]/div/p[2]/strong/text()").extract()[0])
        # now_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        # item['create_time'] = now_time
        # item['update_time'] = now_time
        yield item
