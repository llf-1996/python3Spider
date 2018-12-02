"""
__title__ = ''
__author__ = 'llf'
__mtime__ = '...'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""

import requests
import chardet

# res = requests.get('https://mp.weixin.qq.com/s?__biz=MjM5NDEwMzkxOA==&mid=2660404637&idx=1&sn=8f74e13da505e041f0df2cc45b6a093d&chksm=bdeafa9c8a9d738ae31e920652c696ccbb3718992c7512a22823e8965a77eaa889b06123a193&scene=21#wechat_redirect')

url = 'http://pic.haibao.com/ajax/image:getHotImageList.json?stamp=Thu Nov 29 2018 12:03:02 GMT+0800 (中国标准时间)'
res = requests.get(url)

html = res.content
co = chardet.detect(html)['encoding']
print(co)
# html = html.decode(co)
# with open('1111.html', 'w') as f:
#     f.write(html)
print(html)


