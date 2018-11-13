# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os


def save(html, path):
    '''
    以文件形式保存数据
    :param html: 要保存的数据
    :param path: 要保存数据的路径
    :return:
    '''
    # 判断目录是否存在
    if not os.path.exists(os.path.split(path)[0]):
        # 目录不存在创建，makedirs可以创建多级目录
        os.makedirs(os.path.split(path)[0])
    try:
        # 保存数据到文件
        with open(path, 'wb') as f:
            f.write(html.encode('utf8'))
        print('保存成功')
    except Exception as e:
        print('保存失败', e)


class FalooPipeline(object):
    def process_item(self, item, spider):
        if item:
            chapter_name = item['chapter_name'].split(' ', 1)[1].split('（')[0]
            intro = '小说:' + item['story_name'] + '\t' + '作者:' + item['author_name'] + '\n'
            item1 = {"chapter_name": chapter_name, 'intro': intro, 'chapter_content': item['chapter_content']}
            path = 'feilu/' + item['story_name'] + '/' + item1['chapter_name'] + '.txt'  # 设置路径，也可设为相对路径
            aa = item1.values()
            aa = list(aa)
            aa = '\n'.join(aa)
            save(aa, path)

            # print('############################################')
            # print('本章内容：', item)
            # print('############################################')

        return item
