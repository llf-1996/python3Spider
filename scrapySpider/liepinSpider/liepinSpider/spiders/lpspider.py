# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from liepinSpider.items import LiepinspiderItem


class LpspiderSpider(CrawlSpider):
    name = 'lpspider'
    allowed_domains = ['www.liepin.com']
    start_urls = ['http://www.liepin.com/']

    # 爬取时间
    crawled_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 转换时间格式为字符串
    data_from = '猎聘网'

    rules = (
        Rule(LinkExtractor(allow=r'job/'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'zhaopin/'), follow=True),
    )

    def parse_item(self, response):
        item = LiepinspiderItem()
        job_url = response.url

        selector = Selector(response)
        job_name = selector.xpath('//div[@class="title-info"]/h1/text()').extract()[0].strip()
        company_name = selector.xpath('//div[@class="title-info"]/h3/a/text()').extract()[0].strip()
        company_url = selector.xpath('//div[@class="title-info"]/h3/a/@href').extract()[0].strip()
        work_addr = selector.xpath('//p[@class="basic-infor"]/span/a/text()').extract()[0].strip()
        money = selector.xpath('//p[@class="job-item-title"]/text()').extract()[0].strip()
        publish_time = selector.xpath('//p[@class="basic-infor"]/time/text()').extract()[0]

        item['job_name'] = job_name
        item['job_url'] = job_url
        item['company_name'] = company_name
        item['company_url'] = company_url
        item['work_addr'] = work_addr
        item['money'] = money
        item['publish_time'] = publish_time
        item['crawled_time'] = self.crawled_time
        item['data_from'] = self.data_from

        yield item
