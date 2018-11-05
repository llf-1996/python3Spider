# import requests
# import multiprocessing
# print(multiprocessing.cpu_count())
import urllib.request
response = urllib.request.urlopen("https://www.baidu.com")
print(response.read())

'''
# coding=utf-8
# urllib爬取百度首页并以HTML格式保存到本地

import urllib.request

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
}

request = urllib.request.Request("http://www.baidu.com/", headers=header)
response = urllib.request.urlopen(request)
data = response.read()
print(data)

html = data
with open("baidu.html", "wb") as f:
    f.write(html)

'''



