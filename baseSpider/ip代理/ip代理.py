import urllib.request
from fake_useragent import UserAgent
import requests
import time

ua = UserAgent()
# url = "http://ip.chinaz.com/"
url = "http://www.ip138.com/"


# url = 'http://www.whatismyip.com.tw/'


def urllib_ip():
    '''
    使用urllib设置IP代理
    :return:
    '''
    header = {
        "User-Agent": ua.random
    }
    print(header)
    request = urllib.request.Request(url, headers=header)

    proxyhandler = urllib.request.ProxyHandler({'http': 'http://180.167.162.166:8080'})
    # 创建opener
    opener = urllib.request.build_opener(proxyhandler)
    # install opener
    urllib.request.install_opener(opener)
    # 发起网络请求
    # response = opener.open(url)
    while True:
        try:
            time.sleep(3)
            response = urllib.request.urlopen(request)
            break
        except Exception as e:
            print("异常：", e)
            print("error")
    # 读取数据
    data = response.read().decode("gb2312")
    print(data)


def requests_ip():
    '''
    使用requests设置IP代理
    :return:
    '''
    proxies = {'http': 'http://121.31.153.73:8123'}
    headers = {'User-Agent': ua.random}
    while True:
        try:
            time.sleep(3)
            resp = requests.get(url, headers=headers, proxies=proxies)
            print(resp.content)
            break
        except:
            print("error")

    print(resp.text)
    print(resp.status_code)


if __name__ == '__main__':
    # urllib_ip()  # sucessful
    print("---------" * 8)
    requests_ip()    # sucessful
