'''
爬取百度，并通过url的wd参数控制搜索的页面
'''
# coding=utf-8
import urllib.request

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
}

urlStr = urllib.parse.quote('奇酷')
print(urlStr)
mainUrl = "https://www.baidu.com/s?wd="
realUrl = mainUrl + urlStr

request = urllib.request.Request(realUrl, headers=header)
response = urllib.request.urlopen(request)
data = response.read()
print(data)
html = data.decode("utf-8")
with open("./baidu.html", "w", encoding="utf-8") as f:
    f.write(html)


