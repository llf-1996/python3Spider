'''
爬取格言网： http://www.geyanw.com/
# 下载限速

# 如果我们爬取网站的速度过快，就会面临被 封禁或是造成服务器过载的风险。
# 为了降低这些风险， 我们可以在两次下载之间添加延时，从而对爬虫限速。
# Throttle 类记录了每个域名上次访问的时间，如果当前时间距离上次
# 访问时间小于指定延时，则执行睡眠操作。 我们可以在每次下载之前调用
# Throttle 对爬虫进行限速。
'''

import time
import re
import datetime

import urllib.parse
import urllib.request


class Throttle:
    '''
    限速类
    '''

    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        if self.delay <= 0:
            print("无限速")
            return
        domain = urllib.parse.urlparse(url).netloc  # 获取域名
        last_time = self.domains.get(domain)  # 获取上次爬取时间
        if last_time is not None:
            # 计算等待时间
            wait_sec = self.delay - (datetime.datetime.now() - last_time).seconds
            if wait_sec > 0:
                time.sleep(wait_sec)
        self.domains[domain] = datetime.datetime.now()


# Throttle用法
def download(url, headers={}, retry_count=5):
    print("downloading:", url)
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        print(e)
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, headers, retry_count-1)
        return None
    return html


def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


def link_crawler(seed_url, link_regex):
    url_obj = urllib.parse.urlparse(seed_url)
    # 爬取队列
    crawl_queue = set([seed_url])
    # 记录已爬取过的链接
    crawled_link = set()

    t = Throttle(0.5)
    while crawl_queue:
        url = crawl_queue.pop()
        t.wait(url)
        html = download(url)
        if html is None:
            continue
        crawled_link.add(url)
        for link in get_links(html.decode(errors='ignore')):
            if re.match(link_regex, link):
                real_link = url_obj.scheme + "://" + url_obj.netloc + link
                if real_link not in crawled_link:
                    crawl_queue.add(real_link)


link_crawler('http://www.geyanw.com/', '/mingyanjingju/')

