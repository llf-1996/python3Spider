# -*- coding: utf-8 -*-
# @version : py3
# @Time    : 2020/7/8 4:57 下午
# @Author  : llf
# @File    : omim_spider.py
import random
import re
import math
import time

import requests

TIMEOUT = (10, 30)
UA = [
    # bing
    {
        'user-agent': 'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'
    },
    # 谷歌
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    },
    {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }
]


def get_proxy():
    '''获取66免费代理网的免费代理IP'''
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Connection': 'keep-alive'
    }
    url = 'http://www.66ip.cn/nmtq.php?getnum=1&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip'
    p = requests.get(url, headers=header)
    ip_port = p.text.split('<br />')[0].split('</script>')[-1].strip()
    print('proxy: ={}='.format(ip_port))
    if not ip_port:
        time.sleep(6)
        get_proxy()
    return ip_port


class OmimSpider(object):
    '''omim爬虫'''
    def __init__(self, file_path, open_proxy=False):
        self.header = None
        self.page_size = 200
        self.file_path = file_path
        self.open_proxy = open_proxy
        self.proxy = None

    def get_total_count(self):
        '''
        获取result数据条数
        Returns: list [status， result count]

        '''
        url = 'https://www.omim.org/search?index=entry&start=1&limit=100&retrieve=geneMap&prefix=%23&genemap_exists=true'
        header = random.choice(UA)
        while True:
            try:
                if self.open_proxy:
                    if not self.proxy:
                        proxy_ip = get_proxy()
                        proxy = {
                            'https': 'http://{}'.format(proxy_ip)  # https网站
                        }
                        self.proxy = proxy
                    res = requests.get(url, headers=header, proxies=self.proxy, verify=False, timeout=TIMEOUT,
                                       allow_redirects=False)
                else:
                    res = requests.get(url, headers=header, timeout=60, allow_redirects=False)
                if res.status_code == 200:
                    text = res.text
                    if '<title>Error 403</title>' in text:
                        if not self.open_proxy:
                            return False, '当前ip已被封'
                        self.proxy = None
                        continue
                    re_res = re.search('Results:\s*([\d,]*)\s*entries.', text)
                    if re_res:
                        total_count_str = re_res.group(1)
                        total_count = int(total_count_str.replace(',', ''))
                        res = True, total_count
                    else:
                        res = False, '无法匹配获取数据条数'
                    return res
                else:
                    continue
            except Exception as e:
                print('get page number exception: {}'.format(e))
                if not self.open_proxy:
                    return False, '请求错误'
                self.proxy = None
                continue

    def craw_data(self, current_page):
        '''
        获取单页数据
        Args:
            current_page: 当前页

        Returns: 单页数据字符串

        '''
        url = 'https://www.omim.org/search?index=entry&start={}&limit={}&retrieve=geneMap' \
              '&prefix=%23&genemap_exists=true&format=tsv'.format(current_page, self.page_size)
        header = random.choice(UA)
        while True:
            try:
                if self.open_proxy:
                    if not self.proxy:
                        proxy_ip = get_proxy()
                        proxy = {
                            'https': 'http://{}'.format(proxy_ip)
                        }
                        self.proxy = proxy
                    res = requests.get(url, headers=header, proxies=self.proxy, verify=False, timeout=TIMEOUT,
                                       stream=True, allow_redirects=False)
                else:
                    res = requests.get(url, headers=header, timeout=(10, 30), stream=True)
                if res.status_code == 200:
                    text = res.text
                    if '<title>Error 403</title>' in text:
                        if not self.open_proxy:
                            return False, '当前ip已封'
                        self.proxy = None
                        continue
                    else:
                        return True, text
                else:
                    continue
            except Exception as e:
                print('craw data exception: {}'.format(e))
                if not self.open_proxy:
                    return False, '请求错误'
                else:
                    self.proxy = None
                    continue

    def clean_data(self, text):
        '''
        清理数据
        Args:
            text: 单页数据字符串

        Returns: list

        '''
        text = text.split('Phenotype Mapping Key')[0]
        text = text.split('Johns Hopkins University OMIM, data are provided for research purposes only.')[1]
        text = text.strip()
        header, text = text.split('\n', 1)
        header = header.strip()
        text = text.strip()
        data_list = text.split('\n')
        if self.header == None:
            self.header = header
        return data_list

    def save_data(self, data):
        '''
        保存数据至文本文件，分隔符\t
        Args:
            data: list

        Returns:

        '''
        data.insert(0, self.header)
        data = '\n'.join(data)
        with open(self.file_path, 'w') as f:
            f.write(data)

    def spider_ctr(self):
        '''
        爬虫控制器
        Returns: list [status, message]

        '''
        is_success, res1 = self.get_total_count()
        datas = []
        if is_success:
            total_page = math.ceil(res1/self.page_size)
            total_page = int(total_page)
            print('page_size:', self.page_size, 'total_page:', total_page)
            for i in range(1, total_page+1):
                print('current page:', i)
                is_success, data = self.craw_data(i)
                if is_success:
                    data_list = self.clean_data(data)
                    datas.extend(data_list)
                else:
                    return ['craw data failed', data]
            self.save_data(datas)
            message = 'result:{}, save_count:{}'.format(res1, len(datas))
            return ['success', message]
        else:
            return ['craw data count failed', res1]


if __name__ == '__main__':
    file_path = 'test_omim_data.tsv'  # 结果文件
    # # 不开启代理IP
    # omim_spider_obj = OmimSpider(file_path)
    # 开启代理IP
    omim_spider_obj = OmimSpider(file_path, True)
    res = omim_spider_obj.spider_ctr()
    print(res)
