# -*- coding: utf-8 -*-
import scrapy
import re
from article.items import JobBoleArticleItem,ArticleItemLoader

from scrapy.http import Request
from urllib import parse
from article.utils.common import get_md5
from selenium import webdriver

#信号量
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from article.settings import user_agent_list
import random

import datetime
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']
    # # 不用每次启动都启动Chrome
    # def __init__(self):
    #     self.browser = webdriver.Chrome(executable_path="C:\Program Files\Python36\chromedriver.exe")
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed,signals.spider_closed)
    #
    # def spider_closed(self,spider):
    #     #当爬虫退出的时候退出Chrome
    #     print("spider closed")
    #     self.browser.quit()

    '''
    数据收集(stats Collection)，几乎都是数字类型
    收集伯乐在线所有404的URL以及404的页面数

    scrapy spidermiddlewares httpettor.py 设置一个值handle_httpstatus_list
    
    \site-packages\scrapy\statscollectors.py  打印出stats
    '''
    handle_httpstatus_list = [404]

    def __init__(self):
        self.fail_urls = []
        #信号
        dispatcher.connect(self.handle_spider_closed, signals.spider_closed)

    def handle_spider_closed(self,spider,reason):
        self.crawler.stats.set_value("failed_urls",",".join(self.fail_urls))


    def parse(self, response):
        #数据收集  ,修改URL
        if response.status == 404:
            self.fail_urls.append(response.url)
            self.crawler.stats.inc_value("failed_url")
        '''
        1.获取文章列表页中的文章url并交给scrapy下载后并解析
        2.获取下一页的url并交给scrapy进行下载，下载完后交给parse
        :param response:
        :return:
        '''
        #解析列表页中的所有文章url并交给scrapy下载后并进行解析
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url=post_node.css("img::attr(src)").extract_first("")
            post_url=post_node.css("::attr(href)").extract_first("")

            ##使用随机的User-agent
            # random_index = random.randint(0,len(user_agent_list)-1)
            # random_agent = user_agent_list[random_index]

            yield Request(url=parse.urljoin(response.url,post_url),meta={"front_image_url":image_url},callback=self.parse_detail)

        #提取下一页并交给scrapy进行下载
        next_url=response.css(".next.page-numbers::attr(href)").extract_first('')
        if next_url:
            yield Request(url=next_url,callback=self.parse)

    def parse_detail(self,response):
        # item = JobBoleArticleItem()
        # title=response.css('.entry-header h1::text').extract_first('')
        # create_date=response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].replace("·","").strip()
        # praise_nums=response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        # if praise_nums:
        #     praise_nums = int(praise_nums)
        # else:
        #     praise_nums = 0
        #
        # #收藏
        # fav_nums=response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]
        # match_re=re.match(".*?(\d+).*",fav_nums)
        # if match_re:
        #     fav_nums=int(match_re.group(1))
        # else:
        #     fav_nums=0
        #
        # #评论
        # comments_nums=response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].replace('评论','').strip()
        # if comments_nums:
        #     comments_nums = int(comments_nums)
        # else:
        #     comments_nums = 0
        #
        # #正文
        # content=response.xpath("//div[@class='grid-8']").extract()[0]
        #
        # #标签
        # tag = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag=[element for element in tag if not element.strip().endswith('评论')]
        # tag='-'.join(tag)
        #
        # item['title']=title
        # try:
        #     create_date = datetime.datetime.strptime(create_date,'%Y/%m/%d').date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        # item['create_date'] = create_date
        # item['praise_nums'] = praise_nums
        # item['fav_nums'] = fav_nums
        # item['comments_nums'] = comments_nums
        # item['content'] = content
        # item['tag'] = tag
        # item['url'] = response.url
        # item['url_object_id'] = get_md5(response.url)
        # item['front_image_url'] = [front_image_url]  #图片下载url应该为list类型

        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        #通过item Loader加载item
        item_loader = ArticleItemLoader(item = JobBoleArticleItem(),response=response)
        item_loader.add_css('title','.entry-header h1::text')
        item_loader.add_xpath('create_date','//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_xpath('praise_nums',"//span[contains(@class,'vote-post-up')]/h10/text()")
        item_loader.add_xpath('fav_nums',"//span[contains(@class,'bookmark-btn')]/text()")
        item_loader.add_xpath('comments_nums',"//a[@href='#article-comment']/span/text()")
        item_loader.add_xpath('content',"//div[@class='grid-8']")
        item_loader.add_xpath('tag','//p[@class="entry-meta-hide-on-mobile"]/a/text()')

        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_value('front_image_url',front_image_url)
        item_loader.add_value('front_image_path',"none")

        item = item_loader.load_item()

        yield item



