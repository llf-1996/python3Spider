'''
cookie登录豆瓣网
cookie值可以在浏览器登录后F12打开检查元素选择网络刷新页面然后找到豆瓣首页
复制请求头中的cookie。
'''

import requests

headers = {
    'Cookie': 'cookie值'
}

response = requests.get('https://www.douban.com/', headers=headers)

print(response.text)


