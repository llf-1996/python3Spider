'''
爬取汽车之家
https://www.autohome.com.cn 获取所有车的名称及新手指导价

'''

import urllib.request
import urllib.parse
import re
import time
import os

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


def save(html, path):
    '''
    以文件形式保存HTML
    :param html:
    :return:
    '''

    # link = url.replace("https://www.geyanw.com/", '')
    # link = os.path.split(link)[1]
    # print("++++", path)
    if path.endswith('/'):
        file_path = './html/car/' + "index.html"
    else:
        file_path = './html/car' + path
        if not os.path.exists(os.path.split(file_path)[0]):
            os.makedirs(os.path.split(file_path)[0])
    # print('+++++++', file_path)
    with open(file_path, 'wb') as f:
        f.write(html)


def link_crawler(seed_url, link_regex):
    '''
    控制要爬取网页的url
    :param seed_url:
    :param link_regex:
    :return:
    '''
    # # 分析域名
    # url_obj = urllib.parse.urlparse(seed_url)
    # 爬取队列
    crawl_queue = [seed_url]
    # 记录以爬取过的链接
    crawled_link = set()
    while crawl_queue:
        url = crawl_queue.pop()
        # 爬取网页
        html = download(url)
        if html is None:
            continue
        crawled_link.add(url)
        # 分析域名
        url_obj = urllib.parse.urlparse(url)
        # 保存文件
        # save(html, url_obj.path)
        for link in get_links(html.decode('utf-8', errors="ignore")):
            if re.match(link_regex, link):
                print("##############", link)
                # real_link1 = url_obj.scheme + url_obj.netloc + link
                # print('+++', real_link1)
                if link.startswith("//"):
                    real_link = 'https:' + link
                    if real_link not in crawled_link and real_link not in crawl_queue:
                        crawl_queue.append(real_link)
                    continue
                elif link.startswith('/'):
                    real_link = url_obj.scheme + "://" + url_obj.netloc + link
                    if real_link not in crawled_link and real_link not in crawl_queue:
                        crawl_queue.append(real_link)
                    continue


if __name__ == "__main__":
    link_crawler('https://www.autohome.com.cn/', '^//www.autohome.com.cn/')

'''
具有车的名称及价格的页面URL:
https://www.autohome.com.cn/81/#pvareaid=2042208 
》》》 https://www.autohome.com.cn/81/price.html#pvareaid=3454455



https://www.autohome.com.cn/spec/31848/#pvareaid=3454589
》》》https://www.autohome.com.cn/spec/31803/price.html?pvareaid=101151
'''


