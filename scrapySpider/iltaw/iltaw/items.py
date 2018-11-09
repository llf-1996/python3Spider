# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IltawItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    china_name = scrapy.Field()
    english_name = scrapy.Field()
    img_url = scrapy.Field()
    intro = scrapy.Field()

