import urllib.request
import urllib.parse
import re
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
}


def download(url, headers=header, repeat_time=5):
    '''
    爬取网页
    :param url:
    :param headers:
    :param repeat_time:
    :return:
    '''
    time.sleep(1)
    if (repeat_time <= 0): return None
    print("downloading:" + url)
    request = urllib.request.Request(url, headers=headers)
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.URLError as e:
        if hasattr(e, 'code') and 500 <= e.code < 600:
            return download(url, headers, repeat_time - 1)
        else:
            return None
    html = response.read()
    return html


if __name__ == "__main__":
    url_format = "http://127.0.0.1/places/default/view/{0}"
    country_id = 220
    empty_count = 0
    while True:
        real_url = url_format.format(country_id)
        country_id += 1
        html = download(real_url)
        if html == None:
            empty_count += 1
            if empty_count >= 5:
                break
            else:
                empty_count = 0
