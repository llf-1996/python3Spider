# coding='utf-8'

# 爬取https://www.pexels.com网站的图片
# 异步加载 网页局部刷新 ajax

import requests
from bs4 import BeautifulSoup
import re

headers = {
    'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
}
urls = ['https://www.pexels.com/?page={}'.format(str(i)) for i in range(1, 2)]
print(urls)

photos = []  # 保存图片的url

for url in urls:
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    imgs = soup.select('article.photo-item > a > img')  # 可用火狐浏览器得到css选择器

    for img in imgs:
        photo = img.get('src')  # 获取src属性值
        photos.append(photo)

path = 'E:\\yibutupian\\'

for item in photos:
    data = requests.get(item, headers=headers)
    photo_name = re.findall('\/\d+\/(.*?)\?', item)

    print(photo_name)
    if photo_name:
        with open(path + photo_name[0], 'wb') as fp:
            print(path + photo_name[0])
            fp.write(data.content)
