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
    start_urls = ["http://www.dmm.com/en/rental/-/detail/=/cid=n_611vwdg6298r/"]
    # start_urls = ["file:///tmp/index.html"]
    # def parse(self, response):
    #     filename = response.url.split("/")[-2]
    #     filepath = os.path.join("./tmp/",filename)
    #     with open(filepath, 'wb') as f:
    #         f.write(response.body)

    def parse(self, response):
        sel = Selector(response)
        items = []
        item = DVDDetailItem()
        # item['publisher'] = self.publisher
        # item['id'] = self.id
        item['link'] = response.url
        item['title'] = sel.xpath("//div[@class='page-detail']/div[@class='area-headline group']/div[@class='hreview']/h1/span/text()").extract()
        detail_xpath = "//div[@class='page-detail']/table/tr/td[1]/table/tr[%s]/td[2]/text()"
        for index in xrange( len(DVDDetailItem.m_fields) ):
            item[item.m_fields[index]] = sel.xpath(detail_xpath%(index)).extract()

        # item['rental_date'] = sel.xpath(detail_xpath%(1)).extract()
        # item['production_year'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/table/tr[2]/td[2]/text()").extract()
        print item

        items.append(item)
        return items