# -*- coding: utf-8 -*-
import time

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule, spiders
from scrapy import Request

from faloo.items import FalooItem


class MyspiderSpider(CrawlSpider):
    name = 'myspider'
    allowed_domains = ['b.faloo.com']
    start_urls = ['https://b.faloo.com/f/531576.html']

    rules = (
        # 单本小说url
        Rule(LinkExtractor(allow=r'//b.faloo.com/\w/\d+.html$'), callback='parse_book', follow=True),
    )

    def parse_book(self, response):
        '''
        解析单本小说
        :param response:
        :return:
        '''
        print('##### 单本url:', response.url)
        # 匹配所有章节连接
        chapters = response.xpath("//div[@class='ni_list']//table//a/@href").extract()
        for chapter in chapters:
            # # 不爬取vip章节和不以.html结尾的url
            # if 'vip' in chapter or not chapter.endswith('.html'):
            #     continue
            # # if chapter.startswith('//'):
            # #     chapter = 'https:' + chapter
            # chapter = 'https:' + chapter
            print('+++++++章节：', chapter, 'vip' in chapter)
            time.sleep(1)
            yield Request('https:' + chapter, callback=self.parse_item)

    def parse_item(self, response):
        '''
        匹配章节页
        :param response:
        :return:
        '''
        item = FalooItem()
        print(response.status, '匹配章节详情页。。。。。。。')
        try:
            chapter_name = response.xpath("//div[@id='title']/h1/text()").extract()[0].strip()
            story_name = response.xpath("//div[@id='title_s']/a[1]/text()").extract()[0].strip()
            author_name = response.xpath("//div[@id='title_s']/a[2]/text()").extract()[0].strip()
            # chapter_intro = '小说:' + story_name + '\t' + '作者:' + author_name
            chapter_content = response.xpath("//div[@id='content']//text()").extract()
            a = []
            for content in chapter_content:
                content = content.strip()
                if content:
                    a.append(content)
            print('本章内容：', a)
            chapter_content = '\n'.join(a)
            chapter_content = chapter_content.split('飞卢小说网')[0]

            item['chapter_name'] = chapter_name
            item['story_name'] = story_name
            item['author_name'] = author_name
            item['chapter_content'] = chapter_content
        except Exception as e:
            print('错误：', e)
            item = {}
        yield item


