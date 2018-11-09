# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule, Spider
from scrapy.linkextractors import LinkExtractor

from iltaw.items import IltawItem


class IltawspiderSpider(CrawlSpider):
    name = 'iltawspider'
    allowed_domains = ['www.iltaw.com']

    # ########## start 1.ID遍历
    # # id自增
    # def start_requests(self):
    #     '''
    #     多个目录页
    #     return 单个目录页
    #     '''
    #     for index in range(1, 10):
    #         url = 'http://www.iltaw.com/animal/all?page=%s' % index
    #         yield Request(url, callback=self.parse_index)
    # ################# end 1

    ##############start 2.链接
    start_urls = ['http://www.iltaw.com/animal/all']
    rules = (
        Rule(LinkExtractor(allow=r'/all'), callback='parse_index', follow=True),
    )
    ###############end 2

    def parse_index(self, response):
        print("&&&77目录页：", response.url)
        # 单个目录页的url
        selectList = response.xpath('/html/body/div[1]/div/div[3]/div/div[2]/ul/li/div[2]/h3/a/@href')
        for url in selectList.extract():
            yield Request(url, callback=self.parse_animal)

    def parse_animal(self, response):
        '''
        解析详情页
        :param response:
        :return:
        '''
        items = IltawItem()
        print("++++++++++++++++++++++", response.url)
        china_name = response.xpath("//div[@class='cover-inner-wrap']/div[2]/h3/text()")[0].extract()
        english_name = response.xpath("//div[@class='cover-inner-wrap']/div[2]/h3/span/text()")[0].extract()
        img_url = response.xpath("//div[@class='cover-inner-wrap']/div[2]/div[@class='img']/img/@data-url").extract()[0]
        intro = response.xpath("//div[@class='intro-inner-wrap']/div[2]").xpath('string()').extract()[0].strip()
        intro = re.sub('\s+', ' ', intro)
        items['china_name'] = china_name
        items['english_name'] = english_name
        items['img_url'] = img_url
        items['intro'] = intro
        yield items









