# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagocrawlspider.items import LagouJobItemloader,LagouJobItem
from lagocrawlspider.utils.common import get_md5
from datetime import datetime

import time


#scrapy genspider -t crawl lago www.lagou.com   在lagocrawlspider目录下执行使用crawl模板


class LagoSpider(CrawlSpider):
    name = 'lago'
    allowed_domains = ['www.lagou.com']
    start_urls = ['http://www.lagou.com/']
    rules = (
        Rule(LinkExtractor(allow=("zhaoping/.*",)),follow=True),
        Rule(LinkExtractor(allow=("gongsi/j\d+.html",)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        time.sleep(2)
        item_loader = LagouJobItemloader(item=LagouJobItem(),response=response)
        item_loader.add_css("title",".job-name::attr(title)")
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",get_md5(response.url))
        item_loader.add_css("salary",".job_request .salary::text")
        item_loader.add_xpath("job_city","//*[@class='job_request']/p/span[2]/text()")
        item_loader.add_xpath("work_years", "//*[@class='job_request']/p/span[3]/text()")
        item_loader.add_xpath("degree_need", "//*[@class='job_request']/p/span[4]/text()")
        item_loader.add_xpath("job_type", "//*[@class='job_request']/p/span[5]/text()")
        item_loader.add_css("tags",".position-label li::text")
        item_loader.add_css("publish_time", ".publish_time::text")
        item_loader.add_css("job_advantage", ".job-advantage p::text")
        item_loader.add_css("job_desc", ".job_bt div")
        item_loader.add_css("job_addr", ".work_addr")
        item_loader.add_css("company_name","#job_company dt a img::attr(alt)")
        item_loader.add_css("company_url","#job_company dt a::attr(href)")
        item_loader.add_value("crawl_time",datetime.now())
        items = item_loader.load_item()
        time.sleep(2)
        return items
