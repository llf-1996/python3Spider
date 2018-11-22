"""
__title__ = ''
__author__ = 'llf'
__mtime__ = '...'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import datetime

'''
字体反爬解决方法:
    猫眼电影中影院的的票价数字使用了字体反爬措施，即在源代码中使用数字对应的编码代码该数字，浏览器解析渲染显示正常信息。
    
    补充一点就是你每次访问加载的字体文件中的字符的编码可能是变化的，就是说网站有多套的字体文件。
既然编码是不固定的，那就不能用编码的一一对应关系来处理字体反爬。这里要用到上面说的三方库fontTools，利用fontTools可以获取每一个字符对象，这个对象你可以简单的理解为保存着这个字符的形状信息。而且编码可以作为这个对象的id，具有一一对应的关系。虽然字符的编码是变化的，但是字符的形状是不变的，也就是说这个对象是不变的。

基本思路：
先下载一个字体文件保存到本地（比如叫1.ttf），人工的找出每一个数字对应的编码（安装fontcreate软件打开字体文件），保存到一个字典中，key为字体的编码，value为所代表的字体。
当我们重新访问网页时，同样也可以把新的字体文件下载下来保存到本地ttf（比如叫2.ttf）。网页中的一个数字的编码比如为AAAA，如何确定aa对应的数字。
我们先通过编码aa找到这个字符在2.ttf中的对象，并且把此对象和1.ttf中的对象逐个对比，直到找到相同的对象，然后获取这个对象在1.ttf中的编码，
再通过编码确认是哪个数字。将网页中的字体编码替换为对应字体即可。

'''
import re

import requests
from fontTools.ttLib import TTFont
from fontTools import ttLib
from bs4 import BeautifulSoup


# 抓取maoyan影院
class MaoyanSpider:
    # 页面初始化
    def __init__(self):
        # 请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }

    def getNote(self):
        '''
        解析影院页面
        :return:
        '''

        font1 = TTFont('maoyan.ttf')  # 打开本地字体文件01.ttf
        # font1.saveXML('test.xml')  # 可以将字体文件保存为xml文件便于查看
        # obj_list1 = font1.getGlyphNames()[1:-1]  # 获取所有字符的对象，去除第一个和最后一个
        uni_list1 = font1.getGlyphOrder()[2:]  # 获取所有编码，按数字顺序返回，去除前2个非数字的编码
        # print('base:', uni_list1)
        # 手动确认编码和数字之间的对应关系，保存到字典中
        dict = {'uniF7EE': '8', 'uniEC92': '2', 'uniE665': '1', 'uniEA82': '9',
                'uniE60C': '3', 'uniE28D': '4', 'uniE0D2': '0', 'uniE1D8': '7',
                'uniF78A': '5', 'uniED5E': '6'}

        url = "http://maoyan.com/cinema/17170?poi=152356300"  # 爬取影院网页的URL
        # 获取页面内容
        r = requests.get(url, headers=self.headers)
        # response = html.fromstring(r.text)
        # 使用re匹配网页中字体文件的URL地址
        cmp = re.compile("url\('(//.*?.woff)'\) format\('woff'\)")
        rst = cmp.findall(r.text)
        ttf = requests.get("http:" + rst[0], stream=True)
        with open("maoyan2.ttf", "wb") as pdf:
            pdf.write(ttf.content)
        tt = ttLib.TTFont('maoyan2.ttf')  # 当前网页的字体文件
        # print(tt.getGlyphOrder()[2:])

        # obj_list2 = tt.getGlyphNames()[1:-1]
        uni_list2 = tt.getGlyphOrder()[2:]
        html = r.text  # 得到网页内容
        for uni2 in uni_list2:
            obj2 = tt['glyf'][uni2]  # 获取编码uni2在maoyan2.ttf中对应的对象，tt['glyf']得到所有字符编码的对象
            for uni1 in uni_list1:
                obj1 = font1['glyf'][uni1]
                if obj1 == obj2:  # 通过两个字体文件的字体对象确定映射关系
                    # print(uni2, dict[uni1])  # 打印结果，编码uni2和对应的数字
                    uni2 = uni2.lower()  # 将字体编码转换为小写字母
                    uni2 = uni2[3:]
                    html = html.replace('&#x{};'.format(uni2), dict[uni1])  # 替换字体为正常数字

        # 解析页面提取数据
        # print(html)  # html为替换后的网页内容
        soup = BeautifulSoup(html, 'lxml')
        name = soup.select('h3.name.text-ellipsis')[0]
        # print(name)
        # print(type(name))
        print('影院名字：', name.text)

        address = soup.select('div.address.text-ellipsis')[0]
        print('影院地址：', address.text)

        all_movies = soup.select('div.show-list')
        print('电影数量：', len(all_movies))
        # print(all_movies)
        # 解析单单电影
        for movie in all_movies:
            movie_name = movie.select('h3.movie-name')[0].text
            try:
                movie_score = movie.select('span.score.sc')[0].text
            except:
                movie_score = '无'
            time = datetime.date.today()
            print('###############################################################')
            print("电影名字：", movie_name, "评分：", movie_score, '时间：', time)
            all_movies_count = movie.select('div.plist-container.active table tbody tr')
            # print(all_movies_count)
            if len(all_movies_count):
                for movie_count in all_movies_count:
                    try:
                        count = movie_count.select('td')
                        movie_time = count[0].text.strip()  # 放映时间
                        movie_time = re.sub('\s+', '~', movie_time)
                        movie_language = count[1].text  # 语言版本
                        movie_place = count[2].text  # 语言版本
                        movie_price = count[3].text  # 售价
                        print('放映时间:', movie_time, '语言版本:', movie_language.strip(), '语言版本:', movie_place.strip(), '售价:￥', movie_price.strip())
                    except:
                        print('无场次')
            else:
                print('今日无放映')


if __name__ == "__main__":
    spider = MaoyanSpider()
    spider.getNote()
