# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FalooItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    chapter_name = scrapy.Field()  # 章节名
    story_name = scrapy.Field()  # 小说名
    author_name = scrapy.Field()  # 作者名
    chapter_content = scrapy.Field()  # 本章内容
