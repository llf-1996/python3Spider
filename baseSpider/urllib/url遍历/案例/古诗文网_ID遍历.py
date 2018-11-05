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


def save(html, file_id):
    '''
    以文件形式保存HTML
    :param html:
    :return:
    '''
    file_path = 'html/gushiwen/{}.html'.format(file_id)
    with open(file_path, 'wb') as f:
        f.write(html)


if __name__ == "__main__":
    url_format = "https://so.gushiwen.org/mingju/Default.aspx?p={0}"
    # page_num = 1
    empty_count = 0
    for i in range(1, 201):
        real_url = url_format.format(i)
        html = download(real_url)
        # 保存为文件
        save(html, i)
        # page_num += 1

