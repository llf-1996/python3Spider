'''
http://www.6pifa.net/
爬取商品图片、名称及价格，信息按类别分别放入不同的文本文件
'''

'''
光电鼠标
http://www.6pifa.net/category-874-b0-min0-max0-attr0-1-shop_price-ASC.html
'''
import requests
# from lxml import etree
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17"
}


def download(url, header):
    response = requests.get(url, headers=header)
    response = response.text
    # html = etree.HTML(response)
    soup = BeautifulSoup(response, "lxml")
    goods_items = soup.select('div.goodsItem')
    # print(goods_items)
    # print(len(goods_items))

    # print(goods)
    for goods in goods_items:
        name = goods.select("p > a")
        # print(name)
        goods_name = name[0].get_text()
        # 销量
        # print(goods)
        saled = goods.select("font")
        # print('type:', type(saled))
        # print(saled)
        saled_num = saled[0].text
        # 价格
        price = saled[1].text

        print('商品名字：', goods_name, '销量：', saled_num, '价格：', price)


if __name__ == "__main__":
    for i in range(1, 8):
        print('第%d页' % i)
        url = 'http://www.6pifa.net/category-874-b0-min0-max0-attr0-{}-shop_price-ASC.html'.format(i)
        download(url, header)
