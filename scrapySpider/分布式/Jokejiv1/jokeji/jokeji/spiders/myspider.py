# -*- coding: utf-8 -*-
import datetime
import re

import requests
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
# 分布式
from scrapy_redis.spiders import RedisCrawlSpider

# item
from jokeji.items import JokejiItem


class MyspiderSpider(RedisCrawlSpider):
    name = 'myspider'
    redis_key = 'start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'\?MaxPerPage=33&me_page=\d+'), follow=True),
        Rule(LinkExtractor(allow=r'/jokehtml/\w+?/\d+?.htm'), callback='parse_item', follow=False),
    )

    # def __init__(self, *args, **kwargs):
    #     # Dynamically define the allowed domains list.
    #     domain = kwargs.pop('domain', '')
    #     self.allowed_domains = filter(None, domain.split(','))
    #     # 修改这里的类名为当前类名
    #     super(MyspiderSpider, self).__init__(*args, **kwargs)

    def parse_item(self, response):
        item = JokejiItem()
        title = response.xpath('//div[@class="left_up"]/h1/text()').extract()[1].strip()[3:]
        url = response.url
        content = response.xpath('//span[@id="text110"]//text()').extract()
        the_content = []
        for con in content:
            con = con.strip()
            if con:
                the_content.append(con)
        the_content1 = '\n'.join(the_content)
        publish_time = response.xpath('//div[@class="pl_ad"]/ul/li[3]/i/text()').extract()[0].strip()[5:]
        view_url = response.xpath('//div[@class="left_up"]/i/script/@src').extract()[0]
        res = requests.get('http://www.jokeji.cn' + view_url).text
        print('#####################################')
        print(type(res))
        print(res)
        view_num = re.search(r"hits\+='(\d+?)'", res, re.M)
        print(view_num.group())
        print(view_num.group(0))
        print(view_num.group(1))
        view_num = view_num.group(1)
        print('####################################################')
        print('浏览量：', view_num)
        crawled_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_from = '笑话集'

        item['title'] = title
        item['url'] = url
        item['content'] = the_content1
        item['publish_time'] = publish_time
        item['view_num'] = view_num
        item['crawled_time'] = crawled_time
        item['data_from'] = data_from

        return item
