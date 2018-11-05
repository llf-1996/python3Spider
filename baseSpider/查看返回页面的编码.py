'''
查看爬取网页的编码
'''

import chardet
import requests


def chardet1():
    '''
    查看编码
    :return:
    '''
    r = requests.get('http://www.baidu.com/')
    print(chardet.detect(r.content))


if __name__ == "__main__":
    chardet1()

'''
输出结果：
{'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
'''