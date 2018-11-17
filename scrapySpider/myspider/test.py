import lxml.html
import requests
from fake_useragent import UserAgent

ua = UserAgent()
header = {"User-Agent": ua.random}
html = requests.get("http://www.baidu.com/", headers=header)
html = html.content.decode("utf8")
print(html)
tree = lxml.html.fromstring(html)
mnav = tree.cssselect('div#head .mnav')  # 输出文本内容 # area = td.text_content()
for i in mnav:
    print(i.text)
