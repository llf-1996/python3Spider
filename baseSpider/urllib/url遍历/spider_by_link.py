import urllib.request
import urllib.parse
import re
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
}


def download(url, headers=header, retry_count=5):
    '''
    爬取网页
    :param url:
    :param headers:
    :param retry_count: 重试次数
    :return: 网页内容
    '''
    print("downloading:" + url)
    if retry_count <= 0:
        return None
    request = urllib.request.Request(url, headers=headers)
    try:
        time.sleep(1)
        response = urllib.request.urlopen(request)
        html = response.read()
    except urllib.error.URLError as e:
        print(e)
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, headers, retry_count - 1)
        return None
    return html


def get_links(html):
    '''
    获取页面所有链接
    :param html: 页面内容
    :return:
    '''
    webpage_rex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webpage_rex.findall(html)


def link_crawler(seed_url, link_regex):
    '''
    控制要爬取网页的url
    :param seed_url:
    :param link_regex:
    :return:
    '''
    # 分析域名
    url_obj = urllib.parse.urlparse(seed_url)
    # 爬取队列
    crawl_queue = [seed_url]
    # 记录以爬取过的链接
    crawled_link = set()
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        if html is None:
            continue
        crawled_link.add(url)
        for link in get_links(html.decode('utf-8')):
            if re.match(link_regex, link):
                # real_link1 = url_obj.scheme + url_obj.netloc + link
                # print('+++', real_link1)
                real_link = url_obj.scheme + "://" + url_obj.netloc + link
                if real_link not in crawled_link:
                    crawl_queue.append(real_link)


if __name__ == "__main__":
    link_crawler('http://127.0.0.1/places/', '/places/default/view/|/places/default/index/')


