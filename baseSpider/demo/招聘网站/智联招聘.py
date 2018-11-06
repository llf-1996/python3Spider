'''
爬取智联Python职位信息
    数据库表：编号（自增） 职位名  公司名  工作地点  薪资  发布时间  职位url 公司url  爬取时间
网页数据通过json传递

############# 技术：
请求库：
    requests
应对反爬：
    user-agent  ip代理proxies
    利用time和random进行延时
解析：
    解析json数据获取想要的数据
持久化：
    MySQL
优化：
    进程池Pool
'''

import datetime
import math
from multiprocessing import Pool
import time
import random

import requests
from fake_useragent import UserAgent
from requests import RequestException
# 引入模块
import pymysql  # mysql驱动

ua = UserAgent()
all_nums = 0  # 保存数据总条数


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
    return conn, conn.cursor()


# 创建数据库连接对象和游标对象
conn, my_cursor = mysql_conn()


def get_one_page(url):
    proxies = {'http': 'http://122.115.78.240:38157'}
    header = {
        'User-Agent': ua.random
    }
    try:
        # 添加随机延时
        delay_time = random.uniform(1, 3)
        time.sleep(delay_time)
        response = requests.get(url, headers=header, proxies=proxies)
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.json()
        print(response.status_code)
        return None
    except RequestException as e:
        print(e)
        return None


def parse_one_page(content):
    '''
    分析json数据提取所要数据
    :param content: 每页请求到的json内容
    :return:
    '''
    items = content['data']['results']
    for item in items:
        job_name = item['jobName']
        job_url = item['positionURL']
        company_name = item['company']['name']
        company_url = item['company']['url']
        work_addr = item['city']['display']
        money = item['salary']
        publish_time = item['updateDate']
        # 生成器
        yield {
            'job_name': job_name,
            'job_url': job_url,
            'company_name': company_name,
            'company_url': company_url,
            'work_addr': work_addr,
            'money': money,
            'publish_time': publish_time,
            'crawl_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 转换时间格式为字符串
            'data_from': '智联招聘',
        }


def save_mysql(my_cursor, content):
    '''
    持久化保存到MySQL
    :param my_cursor: 游标对象
    :param content: 要存储的单条数据，dict类型
    :return:
    '''
    # 执行插入sql语句
    i_sql = "insert into jobinfo(job_name, job_url, company_name, company_url, " \
            "work_addr,money, publish_time, crawl_time, data_from) " \
            "values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # print(i_sql)
    try:
        values = list(content.values())  # 将dict_values类型转换为list类型
        res = my_cursor.execute(i_sql, values)  # 参数values可以用列表或元组，返回影响的行数
        # 提交事务，关闭连接
        conn.commit()
    except Exception as e:
        print('数据库保存错误：', e)
        conn.rollback()


def controller(offset=0):
    '''
    爬虫控制器
    :param offset: 页面偏移量
    :return:
    '''
    url = "https://fe-api.zhaopin.com/c/i/sou?start=" + str(offset) + "&pageSize=60&kt=3&kw=Python"
    content = get_one_page(url)

    # 没有抓取到网页内容结束此函数
    if content is None:
        return False

    # 获取数据条数
    global all_nums
    # 返回所有的条数
    if all_nums == 0:
        nums = content['data']['numFound']  # 数据总条数
        all_nums = nums
        return all_nums

    # 解析数据
    res = parse_one_page(content)
    for i in res:
        # print(i)
        # 持久化数据
        save_mysql(my_cursor, i)
    print('保存一页数据')


def main():
    '''
    爬虫入口，调度爬虫
    :return:
    '''
    # 计算总页数
    controller()
    offset = all_nums / 60
    offset = math.ceil(offset)

    ### 进程池
    pool = Pool(6)
    pool.map(controller, [i*60 for i in range(0, offset)])
    conn.close()  # 关闭mysql连接


if __name__ == "__main__":
    main()

