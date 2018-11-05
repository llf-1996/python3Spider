'''
通过网站的sitemap爬取网站
'''
import re
import time

import urllib.request
import urllib.parse

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
            return download(url, headers, repeat_time-1)
        else:
            return None
    html = response.read()
    return html


if __name__ == "__main__":
    html_str = download("http://example.webscraping.com/places/default/sitemap.xml")
    html_str = html_str.decode("utf-8")
    links = re.findall("<loc>(.*?)</loc>", html_str)
    for l in links:
        new_url = l.replace("web-scraping.appspot.com", "example.webscraping.com")
        html = download(new_url)
        print(html)

