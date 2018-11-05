'''
lxml.xpath解析页面
二次匹配问题  lxml的xpath存在匹配问题
'''

from lxml import etree
import lxml.html
from bs4 import BeautifulSoup

text = '''
<div>
    <ul id='a'>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
     <ul id='b'>
         <li class="item-0"><a href="link1.html">11</a></li>
         <li class="item-1"><a href="link2.html">22</a></li>
     </ul>
 </div>
'''

# beautifulsoup  css
soup = BeautifulSoup(text, 'lxml')
all_ul = soup.select('ul')

print(all_ul)
print(type(all_ul))  # list
for i in all_ul:
    all_li = i.select('ul li')
    for li in all_li:
        print('li标签的内容', li.get_text())




print("#################### lxml xpath     ")
### lxml xpath
html = etree.HTML(text)
nodeList = html.xpath('//ul')  # 第一次匹配ul
# print('nodelist：', nodeList)

# 遍历进行二次匹配ul中的li
for i in nodeList:
    ##### 错误内容
    print(etree.tostring(i))  # 输出i的内容
    all_li = i.xpath('//li/a')  # 此处并不是从i中匹配结果，而是html中匹配的
    for li in all_li:
        print('li内容：', li.text)


    # ##### 解决方法
    the_ul = etree.tostring(i)  # 将etree对象转换为字节
    # print('tostring: ', the_ul)
    etree_ul = etree.HTML(the_ul)  # 解析
    all_li = etree_ul.xpath('//li/a/text()')
    print('修改后结果：', all_li)  # 列表形式输出


print("#################### lxml xpath     end")





print("###################### lxml css")
# lxml  css
html = lxml.html.fromstring(text)
nodeList = html.cssselect('ul')  # 第一次匹配ul
# print('nodelist：', nodeList)
print(nodeList)

# 遍历进行二次匹配ul中的li
for i in nodeList:
    contents = i.cssselect('li a')
    for content in contents:
        print('结果：', content.text)
print("###################### lxml css       end")


