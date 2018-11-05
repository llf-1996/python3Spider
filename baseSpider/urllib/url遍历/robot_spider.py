'''
遵守robot爬取网页
'''

import re
import time

import urllib.request
import urllib.parse
import urllib.robotparser


def download(url, headers={}, retry_count=5):
    '''
    爬取网页
    :param url:
    :param headers:
    :param retry_count: 重试次数
    :return: 网页内容
    '''
    if retry_count <= 0:
        return None
    print('downloading:' + url)
    request = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(0.5)
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


# 每次分析出新的连接，先放入‘连接队列’中。
# 从‘连接队列’中获取新的连接，进行下载（访问）
def link_crawler(seed_url, link_regex):
    # 判断是否满足robots协议
    rp = urllib.robotparser.RobotFileParser()  # 获取一个解析器对象。
    rp.set_url("http://127.0.0.1/robots.txt")  # 设置robot文件的地址。
    rp.read()  # 从网上下载robot文件。

    # rp.can_fetch(user_agent, url)# 返回某个user_agent是否有url的访问权限，若无权限，则不能爬取该url。
    # 分析域名
    urlObj = urllib.parse.urlparse(seed_url)

    # 爬取队列
    crawl_queue = [seed_url]
    # 记录已爬取过的链接
    crawled_link = set([])

    while crawl_queue:
        url = crawl_queue.pop()
        if rp.can_fetch('myspider', url):
            print('robots允许访问')
            html = download(url)
        else:
            print('robots禁止访问')
            continue
        if html is None:
            continue

        crawled_link.add(url)
        for link in get_links(html.decode('utf8')):
            if re.match(link_regex, link):

                # realLink = urlObj.scheme + "://" +urlObj.netloc + link
                realLink = link
                if realLink not in crawled_link:
                    crawl_queue.append(realLink)


link_crawler('http://www.qikuedu.com', '.*')
