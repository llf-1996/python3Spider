# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class Liepinspiderv1Pipeline(object):
    def process_item(self, item, spider):
        fp = open('liepin.txt', 'a+', encoding='utf8')
        fp.write('职位名：' + item['job_name'] + '\n')
        fp.write('职位url：' + item['job_url'] + '\n')
        fp.write('公司名：' + item['company_name'] + '\n')
        fp.write('公司url：' + item['company_url'] + '\n')
        fp.write('工作地点：' + item['work_addr'] + '\n')
        fp.write('薪资：' + item['money'] + '\n')
        fp.write('发布时间：' + item['publish_time'] + '\n')
        fp.write('数据源：' + item['data_from'] + '\n')
        fp.write('爬取时间：' + item['crawled_time'] + '\n\n')
        return item

