# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


def mysql_conn():
    '''
    创建MySQL连接
    :return: 游标对象
    '''
    # 定义数据库连接信息
    HOST = 'localhost'
    PORT = 3306
    USER = 'test'
    PASSWORD = '123456'
    DATABASE = 'pythonspider'
    CHARSET = 'utf8'

    # 创建连接数据库对象
    conn = pymysql.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
        charset=CHARSET
    )
    return conn, conn.cursor()


# 创建数据库连接对象和游标对象
conn, my_cursor = mysql_conn()


class JokejiPipeline(object):
    # 创建数据库连接对象和游标对象
    conn, my_cursor = mysql_conn()

    def save_mysql(self, content):
        '''
        持久化保存到MySQL
        :param my_cursor: 游标对象
        :param content: 要存储的单条数据，dict类型
        :return:
        '''
        # 执行插入sql语句
        i_sql = "insert into jokeji(title, url, content, publish_time, " \
                "view_num, crawled_time, data_from) " \
                "values(%s, %s, %s, %s, %s, %s, %s)"
        # print(i_sql)
        try:
            values = list(content.values())  # 将dict_values类型转换为list类型
            res = self.my_cursor.execute(i_sql, values)  # 参数values可以用列表或元组，返回影响的行数
            # 提交事务，关闭连接
            self.conn.commit()
        except Exception as e:
            print('数据库保存错误：', e)
            self.conn.rollback()

    def process_item(self, item, spider):
        print('数据：', item)
        if item['content'].strip():  # 不保存内容为空的数据，有几个内容是图片
            # 持久化数据s
            self.save_mysql(item)
        return item


