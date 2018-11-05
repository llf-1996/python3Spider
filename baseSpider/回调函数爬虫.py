'''
格言网：http://www.geyanw.com/
1.链接爬虫
2.延迟
3.robots
4.proxy
5.depth
6.下载重试次数
7.User-Agent伪装
'''

import urllib.parse
import time
import datetime
import re
import urllib.request
import urllib.robotparser
from lxml import etree


# 根据域名计算并延迟一定的时间
class Throttle:

    def __init__(self, delay):
        # 访问同域名时需要的间隔时间
        self.delay = delay
        # key:netloc,value:lastTime.记录每个域名的上一次访问的时间戳
        self.domains = {}

    # 计算需要的等待时间，并执行等待
    def wait(self, url):
        if self.delay <= 0:
            return

        domain = urllib.parse.urlparse(url).netloc
        lastTime = self.domains.get(domain)

        if lastTime is not None:
            # 计算等待时间
            wait_sec = self.delay - (datetime.datetime.now() - lastTime).seconds
            if wait_sec > 0:
                time.sleep(wait_sec)

        self.domains[domain] = datetime.datetime.now()


# 下载网页
def download(url, headers={}, proxy=None, retry_count=5):
    print('downloading:' + url)
    request = urllib.request.Request(url, headers=headers)

    # 支持代理
    if proxy:
        proxy_handler = urllib.request.ProxyHandler({"http": "http://%(host)s:%(port)d" % proxy})
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        print(e)
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, headers, retry_count - 1)
        return None

    return html


# 获取页面中所有连接
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


# 链接爬虫调度算法
# 每次分析出新的连接，先放入‘连接队列’中。
# 从‘连接队列’中获取新的连接，进行下载（访问）
# seed_url，起始url
# link_regex，链接过滤条件（正则方式）
# maxDepth，可爬取网页的最大深度
# callback，下载到页面后，回调。
def link_crawler(seed_url, link_regex, delay=0.5, bRobots=False, maxDepth=10, callback=None):
    # robots协议
    if bRobots:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url("robot file url")
        rp.read()

        if not rp.can_fetch('QikuSpider', seed_url):
            print('robots 禁止爬取')
            return

    # 分析域名
    urlObj = urllib.parse.urlparse(seed_url)

    # 爬取队列
    crawl_queue = set([seed_url])
    # 记录已爬取过的链接。支持爬取深度
    crawled_link = {}

    t = Throttle(delay)

    while crawl_queue:
        url = crawl_queue.pop()
        t.wait(url)  # 延时
        html = download(url, headers=header)  # 下载页面
        if html is None: continue

        if callback is not None:
            callback(url, html)
        # 获取当前页面的深度
        depth = crawled_link.get(url)
        if depth == None:
            crawled_link[url] = 1
            depth = 1

        if (depth > maxDepth):
            print('max depth')
            continue

        for link in get_links(html.decode(errors='ignore')):
            if re.match(link_regex, link):

                realLink = urlObj.scheme + "://" + urlObj.netloc + link
                if realLink not in crawled_link:
                    crawl_queue.add(realLink)
                    crawled_link[realLink] = depth + 1


# 解析出有用的数据
def parsePage(url, html):
    path = urllib.parse.urlparse(url).path
    if path.find('.html') < 0:
        return

    tree = etree.HTML(html.decode('gb2312', errors='ignore'))
    # allEle = tree.xpath('//body/div/div/div[@class="title"]/h2/text()')
    allEle = tree.xpath('//*[@id="p_left"]/div[1]/div[2]/h2/text()')
    # //*[@id="p_left"]/div[1]/div[2]/h2
    if len(allEle) <= 0:
        return
    print(allEle[0])


if __name__ == "__main__":
    # 连接数据库
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
    }
    link_crawler('http://www.geyanw.com/', '/lizhimingyan/', delay=0, callback=parsePage)
