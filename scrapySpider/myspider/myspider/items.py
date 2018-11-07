# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    lease_type = scrapy.Field()
    suggestion = scrapy.Field()
    bed = scrapy.Field()
    crawled_time = scrapy.Field()
    link = scrapy.Field()
