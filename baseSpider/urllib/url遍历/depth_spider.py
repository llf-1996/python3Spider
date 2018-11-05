'''
我们的爬虫会跟踪所有之前没有访问过的链接。
但是,一些网站会动态生成页面内容，这样就会出现无限多的网页。
比如，网站有一个在线日历功能，提供了可以访问下个月和下一年的链接，
那么下个月的页面中同样会包含访问再下个月的链接，这样页面就会无止境地链接下去。
这种情况被称为爬虫陷阱。

想要避免陷入爬虫陷阱,一个简单的方法是记录到达当前网页经过了多少个链接，也就是深度。
到达最大深度时，爬虫就不再向队列中添加该网页 中的链接了。

要实现这一功能,我们需要修改 crawled_link 变量。
该变量原先只记录访问过的网页链接，现在修改为一个字典，增加了页面深度的记录。
'''

import urllib.parse
import time
import datetime
import re
import urllib.request


class Throttle:

    def __init__(self, delay):
        # 访问同域名时需要的间隔时间
        self.delay = delay
        # key:netloc,value:lastTime.记录每个域名的上一次访问的时间戳
        self.domains = {}

    # 计算需要的等待时间，并执行等待
    def wait(self, url):
        if self.delay <= 0:
            # 没有设置等待时间
            print('delay =', self.delay)
            return

        domain = urllib.parse.urlparse(url).netloc
        lastTime = self.domains.get(domain)

        if lastTime is not None:
            # 计算等待时间
            wait_sec = self.delay - (datetime.datetime.now() - lastTime).seconds
            if wait_sec > 0:
                time.sleep(wait_sec)

        self.domains[domain] = datetime.datetime.now()


def download(url, headers={}, retry_count=5):
    if retry_count <= 0:
        return None
    print('downloading:', url)
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        print(e)
        if hasattr(e, 'code') and 500 <= e.code < 600:
            # 服务器异常，重新爬取，重试次数减1
            return download(url, headers, retry_count - 1)
        return None

    return html


# 获取页面中所有连接
def get_links(html):
    webpage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_regex.findall(html)


# 每次分析出新的连接，先放入‘连接队列’中。
# 从‘连接队列’中获取新的连接，进行下载（访问）
# maxDepth，可爬取网页的最大深度
def link_crawler(seed_url, link_regex, maxDepth=3):
    # 分析域名
    urlObj = urllib.parse.urlparse(seed_url)

    # 爬取队列
    crawl_queue = set([seed_url])
    # 记录已爬取过的链接。支持爬取深度
    crawled_link = {}

    t = Throttle(0.5)

    while crawl_queue:
        url = crawl_queue.pop()
        t.wait(url)
        html = download(url)
        if html is None: continue

        # 获取当前页面的深度
        depth = crawled_link.get(url)
        print("############", url, depth)
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


link_crawler('http://www.geyanw.com/', '/mingyanjingju/', 2)
