# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class DmmJokeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DVDDetailItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    m_fields = ['title','rental_date','production_year','production_country',
                'recorded_time','performers','supervision','production',
                'script','original','details','subtitles','sound','series','studios',
                'genre','movie_id']
    title = Field()
    link = Field()
    img_url = Field()
    rental_date = Field()
    production_year = Field()
    production_country = Field()
    recorded_time = Field()
    performers = Field()
    supervision = Field()
    production = Field()
    script = Field()
    original = Field()
    details = Field()
    subtitles = Field()
    sound = Field()
    series = Field()
    studios = Field()
    genre = Field()
    movie_id = Field()
    brief = Field()