# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from liepinspiderv1.items import Liepinspiderv1Item


class LpspiderSpider(CrawlSpider):
    name = 'lpspider'
    allowed_domains = ['www.liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?key=python']

    # 爬取时间
    crawled_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 转换时间格式为字符串
    data_from = '猎聘网'

    rules = (
        # Rule(LinkExtractor(allow=r'/cjob/.*?html', deny=('init', )), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'/job/.*?html'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'/a/.*?html'), callback='parse_item2', follow=False),
        Rule(LinkExtractor(allow=r'/zhaopin/?.*?key=python.*?', deny=('industries', 'dps', 'salary')), follow=True),
    )

    def parse_item(self, response):
        '''
        解析 / a /..的详情页
        :param response:
        :return:
        '''
        item = Liepinspiderv1Item()
        job_url = response.url

        selector = Selector(response)
        job_name = selector.xpath('//div[@class="title-info"]/h1/text()').extract()[0].strip()
        company_name = selector.xpath('//div[@class="title-info"]/h3/a/text()').extract()[0].strip()
        company_url = selector.xpath('//div[@class="title-info"]/h3/a/@href')
        if company_url:
            company_url = company_url.extract()[0].strip()
        else:
            company_url = "null"
        work_addr = selector.xpath('//p[@class="basic-infor"]/span/a/text()').extract()[0].strip()
        money = selector.xpath('//p[@class="job-item-title"]/text()').extract()[0].strip().strip()
        publish_time = selector.xpath('//p[@class="basic-infor"]/time/text()').extract()[0].strip()

        item['job_name'] = job_name
        item['job_url'] = job_url
        item['company_name'] = company_name
        item['company_url'] = company_url
        item['work_addr'] = work_addr
        item['money'] = money
        item['publish_time'] = publish_time
        item['crawled_time'] = self.crawled_time
        item['data_from'] = self.data_from
        print(job_name)
        print(job_url)
        print(company_name)
        print(company_url)
        print(work_addr)
        print(money)
        print(publish_time)
        print(self.crawled_time)
        print(self.data_from)
        yield item

    def parse_item2(self, response):
        '''
        解析/a/..的详情页
        :param self:
        :param response:
        :return:
        '''
        item = Liepinspiderv1Item()
        job_url = response.url
        company_url = "null"

        selector = Selector(response)
        job_name = selector.xpath('//div[@class="title-info "]/h1/text()').extract()[0].strip()
        company_name = selector.xpath('//div[@class="title-info "]/h3/text()').extract()[0].strip()
        work_addraa = selector.xpath('//p[@class="basic-infor"]/span/text()')
        print('##############################')
        print(type(work_addraa))
        print(work_addraa)
        work_addr = selector.xpath('//p[@class="basic-infor"]/span/text()').extract()[0].strip()
        money = selector.xpath('//p[@class="job-main-title"]/text()').extract()[0].strip()
        publish_time = selector.xpath('//p[@class="basic-infor"]/time/text()').extract()[0].strip()

        item['job_name'] = job_name
        item['job_url'] = job_url
        item['company_name'] = company_name
        item['company_url'] = company_url
        item['work_addr'] = work_addr
        item['money'] = money
        item['publish_time'] = publish_time
        item['crawled_time'] = self.crawled_time
        item['data_from'] = self.data_from
        print(job_name)
        print(job_url)
        print(company_name)
        print(company_url)
        print(work_addr)
        print(money)
        print(publish_time)
        print(self.crawled_time)
        print(self.data_from)
        yield item