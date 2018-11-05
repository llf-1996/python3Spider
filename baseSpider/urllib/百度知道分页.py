'''
爬取百度知道，并通过url的pn参数来进行分页爬取
'''

import urllib.request
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0"
}

real_url = "http://zhidao.baidu.com/search?word=" + urllib.parse.quote(
    "奇酷"
)
real_url = real_url + "&pn={0}"

for i in [0, 20, 30]:
    url = real_url.format(i)
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    response = response.read()
    file_path = "baiduzhidao{}.html".format(i)
    with open(file_path, "wb") as f:
        f.write(response)


