'''
requests  lxml的xpath
爬取ajax页面
通过搜索26个字母得到所有结果并用set去重
'''

import requests
import urllib.parse
from lxml import etree
import string


# 实际的下载流程
def download_inner(url, headers={}, retryTimes=5):
    '''
    网页具体下载器
    :param url:
    :param headers:
    :param retryTimes:
    :return:
    '''
    print('downloading:' + url)
    r = requests.get(url, headers=headers)

    if 500 <= r.status_code < 600:
        if retryTimes > 0:
            return download_inner(url, headers, retryTimes - 1)
        else:
            return None
    else:
        return r


# 正常的网页下载，使用此函数
def download(url, headers={}, retryTimes=5, download=False, filename=None):
    '''
    正常下载器
    :param url:
    :param headers:
    :param retryTimes:
    :return:
    '''
    r = download_inner(url, headers, retryTimes)
    if r is None:
        return None
    if download and filename:
        # 保存到文件
        with open('html/country/{}.html'.format(filename), 'wb') as f:
            f.write(r.content)
        return True
    return r.text


# Json格式下载，使用此函数
def downloadJson(url, headers={}, retryTimes=5):
    '''
    json下载器
    :param url:
    :param headers:
    :param retryTimes:
    :return:
    '''
    r = download_inner(url, headers, retryTimes)
    if r is None:
        return None
    return r.json()


def spiderCountry():
    '''
    爬虫控制器
    :return:
    '''
    crawled_link = set()  # 记录已爬取的URL
    # 对所有的字母进行搜索，string.ascii_uppercase表示26个小写字母
    for word in string.ascii_uppercase:
        # json所需参数
        data = {
            'search_term': word,
            'page_size': 10000,
            'page': 0
        }

        urlFormat = 'http://127.0.0.1/places/ajax/search.json?{0}'
        url = urlFormat.format(urllib.parse.urlencode(data))  # 格式化参数并拼接url
        json = downloadJson(url)  # 下载搜索页
        # print(json)
        # break
        pageNum = json['num_pages']  # 获取搜索的总页数
        #  循环搜索的每一页
        for page in range(0, pageNum):
            data['page'] = page  # 重置ajax请求参数中的页数
            url = urlFormat.format(urllib.parse.urlencode(data))
            json = downloadJson(url)
            # 获取国家详情页面
            pageUrlFormat = 'http://127.0.0.1{0}'
            for item in json['records']:
                # print("$$$$$$$$$$$$$$$", crawled_link)
                # print(len(crawled_link))
                tree = etree.HTML(item['pretty_link'])
                country_name = item['country']
                # print(tree.xpath('//a/@href'))  # 国家详情页的链接，list类型

                realUrl = pageUrlFormat.format(tree.xpath('//a/@href')[0])
                if realUrl in crawled_link:
                    continue
                else:
                    download(realUrl, download=True, filename=country_name)
                    crawled_link.add(realUrl)


if __name__ == "__main__":
    spiderCountry()
