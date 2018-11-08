# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    job_name = scrapy.Field()
    job_url = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    work_addr = scrapy.Field()
    money = scrapy.Field()
    publish_time = scrapy.Field()
    crawled_time = scrapy.Field()
    data_from = scrapy.Field()

