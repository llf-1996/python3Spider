# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


# from scrapy_redis_example.items import ScrapyRedisExampleItem

class MyspiderSpider(RedisCrawlSpider):
    name = 'myspider'
    # allowed_domains = ['127.0.0.1']

    redis_key = 'start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/places/default/index/', deny='/user/'), follow=True),
        Rule(LinkExtractor(allow=r'/places/default/view/', deny='/user/'), callback='parse_item')
    )

    def parse_item(self, response):
        print('###########', response.url)
        i = response.url
        return i
        # i = ScrapyRedisExampleItem()

        # name_css = 'tr#places_country__row td.w2p_fw::text'
        # i['name'] = response.css(name_css).extract()
        # pop_css = 'tr#places_population__row td.w2p_fw::text'
        # i['population'] = response.css(pop_css).extract()

