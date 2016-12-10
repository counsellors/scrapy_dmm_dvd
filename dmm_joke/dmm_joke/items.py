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
    m_fields = ['title','rental_date','production_year','production_country',
                'recorded_time','script','original','details','subtitles','sound','series',
                'movie_id']
    m_type = Field()
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
    average_rating = Field()
    brief = Field()
    slogan = Field()
    create_time = Field()
    update_time = Field()

class DVDDetailListItem(Item):
    m_type = Field()
    link = Field()
    img_url = Field()
    img_desc = Field()
    price = Field()
    create_time = Field()
    update_time = Field()

class ADVDDetailItem(Item):
    m_type = Field()
    title = Field()
    link = Field()
    img_url = Field()
    platform = Field()
    delivery_start_date = Field()
    release_date = Field()
    recorded_time = Field()
    performers = Field()
    supervision = Field()
    series = Field()
    studios = Field()
    lables = Field()
    genre = Field()
    movie_id = Field()
    average_rating = Field()
    brief = Field()
    sample_images = Field()
    total_comment_num = Field()
    create_time = Field()
    update_time = Field()

class ADVDDetailListItem(Item):
    m_type = Field()
    link = Field()
    img_url = Field()
    img_desc = Field()
    price = Field()
    create_time = Field()
    update_time = Field()