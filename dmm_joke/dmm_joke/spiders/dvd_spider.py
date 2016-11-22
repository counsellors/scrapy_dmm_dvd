# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector
from dmm_joke.items import DVDDetailItem


class DvdSpiderSpider(scrapy.Spider):
    name = "dvd_spider"
    allowed_domains = ["dmm.com"]
    start_url_template = 'http://www.dmm.com/rental/-/list/=/sort=ranking/page='
    # start_urls = ["http://www.dmm.com/rental/-/list/=/sort=ranking/page=2/"]
    # start_urls = ["http://www.dmm.com/en/rental/-/detail/=/cid=n_611vwdg6298r/"]
    start_urls = ["file:///tmp/index.html"]
    # def parse(self, response):
    #     filename = response.url.split("/")[-2]
    #     filepath = os.path.join("./tmp/",filename)
    #     with open(filepath, 'wb') as f:
    #         f.write(response.body)

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
        # item['publisher'] = self.publisher
        # item['id'] = self.id
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
        item['brief'] = sel.xpath("//div[@class='page-detail']/table[@class='mg-b12']/tr/td[1]/div/p/text()").extract()

        # item['rental_date'] = sel.xpath(detail_xpath%(1)).extract()
        # item['production_year'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[2]/td[2]/text()").extract()
        print item['brief'][0]

        items.append(item)
        return items