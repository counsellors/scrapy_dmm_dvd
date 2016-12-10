# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.selector import Selector
from dmm_joke.items import DVDDetailItem
from scrapy.spiders import  CrawlSpider,Rule,Spider
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider

class DvdSpiderSpider(RedisCrawlSpider):
    name = "dvd_spider"
    allowed_domains = ["dmm.com"]
    redis_key = 'dvd_spider:start_urls'
    # start_url_template = 'http://www.dmm.com/rental/-/list/=/sort=ranking/page='
    # start_urls = ["http://www.dmm.com/en/rental/-/list/=/article=maker/id=60011/limit=30/view=text/page=2/"]
    # start_urls = ["http://www.dmm.com/en/rental/-/detail/=/cid=n_611vwdg6298r/"]
    field_map = {
                        '貸出開始日：':'rental_date',
                        '製作年：':'production_year',
                        '製作国：':'production_country',
                        '収録時間：':'recorded_time',
                        '出演者：':'performers',
                        '監督：':'supervision',
                        '製作：':'production',
                        '脚本：':'script',
                        '原作：':'original',
                        '詳細：':'details',
                        '字幕：':'subtitles',
                        '音声：':'sound',
                        'シリーズ：':'series',
                        'メーカー：':'studios',
                        'ジャンル：':'genre',
                        '品番：':'movie_id',
                        '平均評価：':'average_rating',
    }


    def get_item_list(self, sel, field_name, item):
        detail_xpath = "./td[2]/a"
        m_field_list = sel.xpath(detail_xpath)
        item[field_name] = []
        for m_field in m_field_list:
            items = []
            items.append(m_field.xpath("text()").extract()[0])
            items.append(m_field.xpath("@href").extract()[0])
            item[field_name].append(items)

    def parse(self, response):
        sel = Selector(response)
        item = DVDDetailItem()
        item['m_type'] = 'dvd'
        item['link'] = response.url
        item['img_url'] = sel.xpath("//div[@class='page-detail']/table/tr/td[1]/div/div[@id='sample-video']/a/img/@src").extract()
        item['title'] = sel.xpath("//div[@class='page-detail']/div[@class='area-headline group']/div[@class='hreview']/h1/span/text()").extract()
        detail_xpath = "//div[@class='page-detail']/table/tr/td[1]/table/tr"
        item_list_types = [ 'performers','supervision','production','studios','genre']
        for table_row in sel.xpath(detail_xpath):
            r_row_key = table_row.xpath('./td[@class="nw"][@align="right"]/text()').extract()
            if len(r_row_key) != 0:
                row_key = str(r_row_key[0].encode('utf-8')).strip()
                field_name = self.field_map.get(row_key)
                if field_name is not None:
                    if field_name in item_list_types:
                        self.get_item_list(table_row, field_name, item)
                    else:
                        if field_name != 'average_rating':
                            item[field_name] = table_row.xpath('./td[2]/text()').extract()[0]
                        else:
                            rating_img = table_row.xpath('./td[2]/img/@src').extract()[0]
                            try:
                                item[field_name] = float(rating_img.split('/')[-1].split('.')[0].replace('_','.'))
                            except Exception, e:
                                item[field_name] = rating_img

        item['slogan'] = sel.xpath("//div[@class='page-detail']/table[@class='mg-b12']/tr/td[1]/div[@class='clear tx14 lh4 bold']/text()").extract()
        item['brief'] = sel.xpath("//div[@class='page-detail']/table[@class='mg-b12']/tr/td[1]/div/p/text()").extract()
        yield item