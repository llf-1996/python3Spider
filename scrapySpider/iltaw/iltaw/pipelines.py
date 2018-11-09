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


def save_mysql(my_cursor, content):
    '''
    持久化保存到MySQL
    :param my_cursor: 游标对象
    :param content: 要存储的单条数据，dict类型
    :return:
    '''
    # 执行插入sql语句
    i_sql = "insert into animalworld(china_name, english_name, img_url, intro) values(%s, %s, %s, %s)"
    # print(i_sql)
    try:
        values = list(content.values())  # 将dict_values类型转换为list类型
        res = my_cursor.execute(i_sql, values)  # 参数values可以用列表或元组，返回影响的行数
        # 提交事务，关闭连接
        conn.commit()
    except Exception as e:
        print('\n\n数据库保存错误：', e)
        conn.rollback()


# 创建数据库连接对象和游标对象
conn, my_cursor = mysql_conn()


class IltawPipeline(object):
    def process_item(self, item, spider):
        print('信息：', item)
        return item


class mysqlPipeline(object):
    '''
    保存MySQL数据库
    '''
    def process_item(self, item, spider):
        save_mysql(my_cursor, item)
        return item
