'''
通过id遍历爬取猫眼top100的视频

requests下载网页
re解析网页
MySQL存储
文件存储

'''
import json
from multiprocessing import Pool
import re

import requests
from requests.exceptions import RequestException  # 异常处理
# 引入模块
import pymysql  # mysql驱动


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

    # # 获取游标对象
    # my_cursor = conn.cursor()
    return conn


# 创建数据库游标对象
conn = mysql_conn()
# 获取游标对象
my_cursor = conn.cursor()


def get_one_page(url):
    '''
    下载网页数据
    :param url:
    :return: 成功返回html内容否则返回None
    '''
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
    }
    try:
        response = requests.get(url, headers=header)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        print(e)
        return None


def parse_one_page(html):
    '''
    解析网页数据
    :param html:
    :return:
    '''
    pattern = re.compile('<dd>.*?board-index.*?">(\d+)</i>.*?data-src="(.*?)".*?class="name"><a'
                         '.*?>(.*?)</a>.*?"star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?"score">.*?'
                         '"integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    # re.S可以使.匹配包含\n换行符在内的所有字符
    items = re.findall(pattern, html)
    # print(items)
    for item in items:
        yield {
            'the_index': item[0],
            'image_url': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'the_time': item[4].strip()[5:],
            'score': item[5].strip() + item[6].strip()
        }


def write_to_file(content):
    '''
    持久化保存到txt文件
    :param content: 字典对象
    :return:
    '''
    # encoding ensure_ascii设置文件中的中文正常显示
    with open('maoyanTop100.txt', 'a', encoding='utf8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def save_mysql(my_cursor, content):
    '''
    持久化保存到MySQL
    :param my_cursor: 游标对象
    :param content: 要存储的数据，dict类型
    :return:
    '''
    # 执行插入sql语句
    i_sql = "insert maoyantop100(the_index, image_url, title, actor, the_time, score) " \
            "values(%s, %s, %s, %s, %s, %s)"
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
    '''
    主函数
    :return:
    '''
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    # print(html)
    res = parse_one_page(html)
    try:
        # 持久化一页数据
        for item in res:
            write_to_file(item)
            # save_mysql(my_cursor, item)
        print('成功持久化一页数据')
    except Exception as e:
        print(e)
        print('数据持久化出错')


if __name__ == '__main__':
    # for i in range(10):
    #     main(i*10)

    ### 进程池
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    conn.close()  # 关闭连接


