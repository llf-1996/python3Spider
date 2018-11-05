# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
'''
class ArticlePipeline(object):
    def process_item(self, item, spider):
            with open(r"E:\python\python代码\scrapy\four week\article\bole.txt", 'a+', encoding='utf-8') as f:
            f.write('title:' + item['title'] + '\n')
            f.write('create_date:' + item['create_date'] + '\n')
            f.write('praise_nums:' + item['praise_nums'] + '\n')
            f.write('fav_nums:' + item['fav_nums'] + '\n')
            f.write('comments_nums:' + item['comments_nums'] + '\n')
            f.write('content:' + item['content'] + '\n')
            f.write('url:' + item['url'] + '\n')
            f.write('url_object_id:' + item['url_object_id'] + '\n')
            f.write('front_image_url:' + str(item['front_image_url']) + '\n')
            f.write('front_image_path:' + item['front_image_path'] + '\n')
            f.write('tag:' + item['tag'] + '\n' * 10)
        return item


'''
import codecs
import json
from scrapy.pipelines.images import ImagesPipeline  #自动下载图片
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlePipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出
    def __init__(self):
        self.file=codecs.open('article.json','w',encoding='utf-8')
    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item
    def spider_closed(self,spider):
        self.file.close()


class JsonExporterPipeline(object):
#     调用scrapy提供的json export导出json文件
    def __init__(self):
        self.file = open('articleexport.json','wb')
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item


class mysqlPipeline(object):
    #采用同步机制写入MySQL
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1','root','root','articlespider',charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self,item,spider):
        insert_sql="""
            insert into jobbole_article(title,create_date,praise_nums,fav_nums,comments_nums,content,tag,url,url_object_id,front_image_url,front_image_path)
            value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        #execute、commit同步操作
        self.cursor.execute(insert_sql,(item['title'],item['create_date'],item['praise_nums'],item['fav_nums'],item['comments_nums'],item['content'],item['tag'],item['url'],item['url_object_id'],item['front_image_url'][0],item['front_image_path']))
        self.conn.commit()
        return item


#mysql插入异步化
class MysqlTwistedPipline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWORD'],
            charset= 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparms)
        return cls(dbpool)

    def handle_error(self,failure,item,spider):
        #处理异步插入异常
        print(failure)

    #在dbpool中拿出一个cursor
    def do_insert(self,cursor,item):
        #执行具体插入
        insert_sql = """
                  insert into jobbole_article(title,create_date,praise_nums,fav_nums,comments_nums,content,tag,url,url_object_id,front_image_url,front_image_path)
                  value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
              """
        cursor.execute(insert_sql, (item['title'], item['create_date'], item['praise_nums'], item['fav_nums'], item['comments_nums'],item['content'], item['tag'], item['url'], item['url_object_id'], item['front_image_url'][0],item['front_image_path']))
        return item

    def process_item(self,item,spider):
        #使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert,item)
        query.addErrback(self.handle_error,item,spider)   #处理异常


#自动下载图片
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_path" in item:
            for ok,value in results:
                image_file_path = value['path']
            item['front_image_path'] = image_file_path
        return item



