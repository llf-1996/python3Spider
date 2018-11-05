'''
百度首页爬取指定字段
'''
import lxml.html
import requests
from fake_useragent import UserAgent

ua = UserAgent()
header = {
    "User-Agent": ua.random
}
html = requests.get("http://www.baidu.com/", headers=header)
html = html.content.decode("utf8")
# print(html)
tree = lxml.html.fromstring(html)
# mnav = tree.cssselect('div#head div:nth-of-type(3) a.mnav:nth-of-type(1)')
mnav = tree.cssselect('#head .mnav')
# area = td.text_content()
for i in mnav:
    print(i.text)
