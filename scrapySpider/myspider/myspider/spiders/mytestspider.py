# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from myspider.items import MyspiderItem
from scrapy.selector import Selector


class MytestspiderSpider(CrawlSpider):
    name = 'mytestspider'
    allowed_domains = ['sh.xiaozhu.com']
    start_urls = ['http://sh.xiaozhu.com/']
    # 爬取时间
    crawled_time = datetime.datetime.now().date().strftime("%Y-%m-%d")

    rules = (
        Rule(LinkExtractor(allow=r'fangzi/'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'search-duanzufang'), follow=True),
    )

    def parse_item(self, response):
        item = MyspiderItem()
        print("######################")
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
        print(response.url)
        selector = Selector(response)
        title = selector.xpath('//h4/em/text()').extract()[0]
        # title1 = selector.xpath('//h4/em/text()')
        # print('#########################')
        # print(title1)
        # print(type(title1))
        # print(title1[0].extract())
        # print('#####################')
        address = selector.xpath('//p/span[@class="pr5"]/text()').extract()[0].strip()
        price = selector.xpath('//*[@id="pricePart"]/div[1]/span/text()').extract()[0]
        lease_type = selector.xpath('//*[@id="introduce"]/li[1]/h6/text()').extract()[0]
        suggestion = selector.xpath('//*[@id="introduce"]/li[2]/h6/text()').extract()[0]
        bed = selector.xpath('//*[@id="introduce"]/li[3]/h6/text()').extract()[0]

        item['title'] = title
        item['address'] = address
        item['price'] = price
        item['lease_type'] = lease_type
        item['suggestion'] = suggestion
        item['bed'] = bed
        item['crawled_time'] = self.crawled_time

        yield item

