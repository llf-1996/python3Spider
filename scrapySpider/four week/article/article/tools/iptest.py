import requests
from fake_useragent import UserAgent
ua = UserAgent()

'''
http://223.241.78.55:18118

'''


proxies = {
  "http": "http://211.147.67.150:80",
  "https": "http://121.237.137.80:18118",
}
header = {
    'User-Agent':ua.random
    }
for i in range(10):
    try:
        response = requests.get("http://www.baidu.com",headers=header,proxies=proxies,timeout=500)
        print(response.status_code)
        # print(response.text)
        with open('bd.html','w',encoding="utf8") as f:
            f.write(response.text)
        break
    except:
        print("error")
        continue



