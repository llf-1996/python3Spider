"""
__title__ = ''
__author__ = 'llf'
__mtime__ = '...'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

'''
微博登录cookie池示例
'''

import random
import json
import time

from selenium import webdriver
from fake_useragent import UserAgent
import requests
import pymysql
# from bs4 import BeautifulSoup
#  import hashlib

class CookiesPool:
    def __init__(self):
        self.ua = UserAgent()
        host = 'localhost'
        port = 3306
        dbname = 'pythonspider'
        user = 'test'
        pwd = '123456'
        self.id_list = []
        try:
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=pwd, db=dbname, charset='utf8')
            # self.conn = pymysql.connect(host='localhost', port=3306, db='sundb', user='root', passwd='123456',charset='utf8')

            self.cur = self.conn.cursor()
            self.get_from_db()
        except Exception as e:
            print(e)
            self.close()
        self.driver = webdriver.Chrome(r"E:\myplugins\chromedriver.exe")

    def get_from_db(self):
        # 从数据库中读取已有的cookie，并检验其有效性
        strsql = 'select * from tbcookies'
        self.cur.execute(strsql)
        results = self.cur.fetchall()
        for item in results:
            username = item[1]
            cookies = item[3]
            home_url = item[4]
            if self.check_cookies(username, cookies, home_url):
                self.id_list.append(username)
            else:
                self.delCookies(username)
            time.sleep(2)

    def gen_cookies(self, loginname, password):
        # 根据帐号密码生成登陆后的 cookie
        if loginname not in self.id_list:
            try:
                self.driver.delete_all_cookies()
                self.driver.set_window_size(1124, 850)
                self.driver.get('http://www.weibo.com/login.php')
                time.sleep(2)
                print('输入用户名....')
                self.driver.find_element_by_id('loginname').clear()
                self.driver.find_element_by_id('loginname').send_keys(loginname)
                time.sleep(2)
                print('输入密码......')
                self.driver.find_element_by_name('password').clear()
                self.driver.find_element_by_name('password').send_keys(password)

                time.sleep(2)
                print('开始登录....')
                self.driver.find_element_by_xpath('//*[@id="pl_login_form"]/div/div[3]/div[6]/a').click()
                time.sleep(3)
                print('获取cookie....')
                cookies = self.driver.get_cookies()
                print('cookie:', cookies)
                home_url = self.driver.current_url
                return (cookies, home_url)
            except Exception as e:
                print('登录失败！', e)
                return None

    def check_cookies(self, username, cookies, home_url):
        # 检验cookies是否有效
        try:
            cookies = json.loads(cookies)
            print('cookie type:', type(cookies))
        except Exception as e:
            print('cookie 不合法', username)
            self.delCookies(username)
            print('删除 cookie ', username)
            return False

        headers = {'User-Agent': self.ua.random}  # 定制请求头
        try:
            print('check ', username)
            cookies = requests.utils.cookiejar_from_dict(cookies)
            response = requests.get(url=home_url, headers=headers, cookies=cookies, allow_redirects=False, timeout=5)
            print('code:', response.status_code)
            if response.status_code == 200:
                print('cookie 有效 ', username)
                return True
            else:
                print('cookie 失效', username)
                return False
        except:
            return False

    def save(self, username, passwd, cookies, home_url):
        '''
        cookies 存储到数据库
        :param username:  用户名
        :param password:  密码
        :param cookies:   cookie
        :param home_url:  登录后的页面url
        :return:
        '''
        print('###1', cookies)
        if username not in self.id_list:
            try:
                dict = {}
                for cookie in cookies:
                    print('#######2', cookie)
                    dict[cookie['name']] = cookie['value']
                cookies = json.dumps(dict)
                print('cookies:', cookies)
                strsql = "insert into tbcookies(username, passwd, cookies, home_url) " \
                         "VALUES(%s,%s,%s,%s)"
                params = (username, passwd, cookies, home_url)
                self.cur.execute(strsql, params)
                self.conn.commit()
                self.id_list.append(username)  # 添加用户名到list中，方便提取数据
                print('save cookie ', username)
            except Exception as e:
                print(e)
                self.close()

    def get_proxy(self):
        '''
        # 随机提取可用的 cookies
        :return:
        '''

        if len(self.id_list) <= 0:
            return None
        username = random.choice(self.id_list)
        strsql = 'select*from tbcookies where username="' + username + '"'
        self.cur.execute(strsql)
        result = self.cur.fetchone()
        if result != None:
            username = result[1]
            cookies = result[3]
            home_url = result[4]
            # cookie验证是否可用
            if self.check_cookies(username, cookies, home_url):
                try:
                    the_cookies = json.loads(cookies)
                    return the_cookies
                except Exception as e:
                    print('cookie 不合法', username)
                    self.delCookies(username)  # 删除数据库中不合法cookie
                    return self.get_proxy()  # 重新获取cookie
            else:
                self.delCookies(username)
                return self.get_proxy()
        else:
            return self.get_proxy()

    def delCookies(self, username):
        '''
        # 删除指定的无效 cookies
        :param username:
        :return:
        '''
        strsql = 'delete from tbcookies where username="' + username + '"'
        self.cur.execute(strsql)
        self.conn.commit()
        print('del cookies:', username)

    def close(self):
        '''
        # 关闭数据库
        :return:
        '''
        try:
            self.cur.close()
            self.conn.close()
            self.driver.close()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pool = CookiesPool()
    # 保存一个cookie
    username = '*****'
    password = '****'
    cookies, home_url = pool.gen_cookies(username, password)
    if cookies != None:
        pool.save(username, password, cookies, home_url)
    # 获取一个cookie
    one_cookie = pool.get_proxy()
    print('提取到的cookie为：', one_cookie)
    pool.close()


