'''
爬取前程无忧的上海地区的Python职位信息

    编号（自增） 职位名  公司名  工作地点  薪资  发布时间  职位url 公司url  爬取时间

    静态页面

技术：
requests
beautifulsoup
xpath

'''
import datetime
from multiprocessing import Pool
import time
import random

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import RequestException
# 引入模块
import pymysql  # mysql驱动

ua = UserAgent()


def mysql_conn():
    '''
    创建MySQL连接
    :return: 游标对象
    '''
    # 定义数据库连接信息
    HOST = 'localhost'
    PORT = 3306
    USER = 'root'
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
    return conn


# 创建数据库游标对象
conn = mysql_conn()
# 获取游标对象
my_cursor = conn.cursor()


def get_one_page(url):
    header = {
        'User-Agent': ua.random
    }
    try:
        # 添加随机延时
        delay_time = random.uniform(0, 2)
        time.sleep(delay_time)
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.content.decode('gbk')
        return None
    except RequestException as e:
        print(e)
        return None


def parse_one_page(content):
    soup = BeautifulSoup(content, 'lxml')
    # 匹配class为el和title的div的class为el的所有div兄弟标签，返回list列表
    items = soup.select("#resultList > div.el.title ~ div.el")
    # print(items)
    for item in items:
        job_name = item.select("p.t1 > span > a")[0].text.strip()
        job_url = item.select("p.t1 > span > a")[0].get("href").strip()
        company_name = item.select("span.t2 > a")[0].text.strip()
        company_url = item.select("span.t2 > a")[0].get("href").strip()
        work_addr = item.select("span.t3")[0].get_text().strip()
        money = item.select("span.t4")[0].get_text().strip()
        publish_time = item.select("span.t5")[0].get_text().strip()
        yield {
            'job_name': job_name,
            'job_url': job_url,
            'company_name': company_name,
            'company_url': company_url,
            'work_add': work_addr,
            'money': money,
            'publish_time': publish_time,
            'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_from': '前程无忧',
        }
    # print(items)
    # print(len(items))
    # print(type(items))
    # return items


def save_mysql(my_cursor, content):
    '''
    持久化保存到MySQL
    :param my_cursor: 游标对象
    :param content: 要存储的数据，dict类型
    :return:
    '''
    # 执行插入sql语句
    i_sql = "insert into jobinfo(job_name, job_url, company_name, company_url, " \
            "work_addr,money, publish_time, crawl_time, data_from) " \
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # print(i_sql)
    try:
        values = list(content.values())  # 将dict_values类型转换为list类型
        res = my_cursor.execute(i_sql, values)  # 可以用列表或元组
        # print(res)  # 返回影响的行数
        # 提交事务，关闭连接
        conn.commit()
    except Exception as e:
        print('数据库保存错误：', e)
        conn.rollback()


def main(offset):
    url = "https://search.51job.com/list/030200,000000,0000,00,9,99,python,2,{}.html".format(offset)
    content = get_one_page(url)
    # 没有抓取到网页内容结束函数
    if content is None:
        return False
    # print(content)
    res = parse_one_page(content)
    for i in res:
        print(i)
        save_mysql(my_cursor, i)


if __name__ == "__main__":
    ### 进程池
    pool = Pool()
    pool.map(main, [i for i in range(1, 71)])
    conn.close()  # 关闭连接


