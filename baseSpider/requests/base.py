import requests
import json

r = requests.get('http://www.baidu.com')
html = r.content
# html = html.decode('utf-8')
print(html)
print(r.text)
print(r.encoding)
# with open("baidu.html", "w", encoding="utf-8") as f:
#     f.write(html)
# print(html)

'''
# 请求头User-Agent
import requests


def userAgent():
    headers = {'user-agent': 'my-app/0.0.1'}
    r = requests.get('http://www.baidu.com/', headers=headers)
    
    
userAgent()
'''


'''
#上传文件
import requests,json
files={
    'file':open('test.txt','rb')
}
r=requests.post('http://httpbin.org/post',files=files)
print(r.text)

'''

'''
#cookies
url ='http://httpbin.org/cookies'
cookies=dict(cookies_are='working')
r=requests.get(url,cookies=cookies)
print(r.text)
'''

'''
#请求超时
url='http://github.com'
r=requests.get(url,timeout=1000)
print(r.text)
'''

'''
#持久会话
s=requests.Session()
s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
r=s.get('http://httpbin.org/cookies')
print(r.text)
'''

'''
#代理
proxies={
    'https':'http://41.118.132.69:4433'
}
r=requests.get('https://www.baidu.com',proxies=proxies)
print(r.status_code)
'''


'''
# 解析json
import requests

def json1():
    r = requests.get('https://github.com/timeline.json')
    r.raise_for_status() # 在响应失败时，此会抛出异常
    print(r.status_code)
    print(r.json())


json1()
'''