import requests
import json


def dataGet():
    # 带参数的GET请求
    r = requests.get('http://www.baidu.com/s', params={"wd": "中国"})
    print(r.text)


def dataPost():
    # post请求带参数
    payload = {
        'hello': 'world'
    }
    r = requests.post('http://httpbin.org/post', data=json.dumps(payload))
    print(r.url)
    print(r.text)


if __name__ == "__main__":
    dataGet()  # get传参
    # dataPost()  # post传参
