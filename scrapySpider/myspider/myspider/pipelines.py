# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        fp = open('xiaozhu.txt', 'a+', encoding='utf8')
        fp.write('标题：' + item['title'] + '\n')
        fp.write('地址：' + item['address'] + '\n')
        fp.write('价格￥：' + item['price'] + '\n')
        fp.write('出租类型：' + item['lease_type'] + '\n')
        fp.write('租住建议：' + item['suggestion'] + '\n')
        fp.write('床：' + item['bed'] + '\n')
        fp.write('爬取时间：' + item['crawled_time'] + '\n\n')
        return item
