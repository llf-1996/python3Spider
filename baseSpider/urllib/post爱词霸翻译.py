import urllib.request
import urllib.parse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
}

real_url = "http://zhidao.baidu.com/search?word=" + urllib.parse.quote(
    "奇酷"
)



