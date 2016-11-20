# -*- coding: utf-8 -*-
import scrapy
import os

class DvdSpiderSpider(scrapy.Spider):
    name = "dvd_spider"
    allowed_domains = ["dmm.com"]
    start_url_template = 'http://www.dmm.com/rental/-/list/=/sort=ranking/page='
    start_urls = [
    	"http://www.dmm.com/rental/-/list/=/sort=ranking/page=2/"]

    def parse(self, response):
        filename = response.url.split("/")[-2]
        filepath = os.path.join("./tmp/",filename)
        with open(filepath, 'wb') as f:
            f.write(response.body)

  def parseDetail(self, response):
    sel = Selector(response)
    items = []
    item = DmmQueryItem()
    item['publisher'] = self.publisher
    item['id'] = self.id
    item['link'] = response.url
    item['filename'] = "_NonExists"
    item['directory'] = self.directory
    item['cover'] = sel.xpath('//a[@name="package-image"]/@href').extract()[0]
    actress_list = sel.xpath('//span[@id="performer"]/a/text()').extract()
    for actress in actress_list:
      item['actress'] = actress

    item['title'] = sel.xpath('//h1[@id="title"]/text()').extract()[0]
    item['productId'] = sel.xpath(u'//table[@class="mg-b20"]/tr/td[contains(text(),"品番：")]/following-sibling::td/text()').extract()[0]
    thumbnail_list = sel.xpath('//div[@id="sample-image-block"]/a/img/@src').extract()
    thumbnail_large_list = []
    for thumbnail in thumbnail_list:
      thumbnail_large = thumbnail.replace('-', 'jp-')
      thumbnail_large_list.append(thumbnail_large)

    item['thumbnails'] = thumbnail_large_list

    print item['cover']
    print item['actress']
    print item['title']
    print item['productId']
    print item['link']
    print item['thumbnails']
    items.append(item)
    return items