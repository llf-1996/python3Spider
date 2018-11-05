
'''
正则查找
'''

from bs4 import BeautifulSoup
import requests


# 处理不完整的html
def brokenHtml():
    broken_html = '<ul class=country> <li>Area</li> <li>Population</ul>'
    soup = BeautifulSoup(broken_html, 'html.parser')
    fixed_html = soup.prettify()
    print(fixed_html)


# bs4find()查找节点
def find():
    broken_html = '<ul class=country> <li>Area</li> <li>Population</ul><li/>'
    soup = BeautifulSoup(broken_html, 'html.parser')
    ul = soup.find('ul', attrs={'class': 'country'})  # find()返回第一个结果
    li = soup.find('li')
    print(ul)
    print(li)
    print(ul.find_all('li'))  # 返回列表


def example():
    url = 'http://example.webscraping.com/places/default/view/Ethiopia-71'
    html = requests.get(url)  # 最基本的GET请求
    soup = BeautifulSoup(html.text, 'html.parser')
    # soup.find('li', attrs={})
    tr = soup.find(attrs={'id': 'places_area__row'})
    td = tr.find(attrs={'class': 'w2p_fw'})
    area = td.text  # 标签内容
    print(area)
    print(tr.get('id'))  # 标签的id属性值
    print(tr.attrs)  # 获取所有属性


example()

'''
python3之beautifulsoup4

################# 遍历文档树
# 节点内容
soup.p.string  
# 获取p标签的内容，如果tag只有一个navigablesting类型子节点，那么这个tag可以使用.string得到子节点内容，如果超过一个，返回None
例：<div>div-content<span>span-content</span></div>此标签还有一个span标签也有一个navigablesting类型
# 多个内容
.strings属性，获取所有内容，返回一个generator(包含空白字符)
.stripped_strings属性，获取所有内容，返回一个generator(去除空白字符)
例：
print(list(soup.div.strings)) 
结果为：['div-content', 'span-content']

# 直接子节点
.contents 将tag的子节点以列表的方式输出,包含当前标签的内容
.children 将tag的子节点以list_iterator的方式输出
例：
soup.div.children  # 返回div标签的内容和div标签的子标签
soup.div.contents

# 所有子孙节点
.descendants属性 对所有子节点递归
例：
soup.div.descendants  # 返回div标签的内容和div标签的子标签和子标签的内容

# 父节点
.parent  获取父节点

# 全部父节点
.parents 获取全部父节点

# 兄弟节点  ----换行也算一个兄弟节点
.next_sibling  下一个兄弟节点
.previous_sibling  下一个兄弟节点
例：
repr(soup.p.next_sibling)

# 全部兄弟节点  ----换行也算一个兄弟节点
.next_siblings  下一个兄弟节点
.previous_siblings  下一个兄弟节点

# 前后节点  ----换行也算一个节点,当前tag的navagablestring也算一个节点
.next_element 后一节点
.previous_element 前一节点 知道html标签
例：
soup.p.next_element.next_element
# 所有前后节点  
.next_elements 所有后节点
.previous_elements 所有前节点



################# 搜索文档树
# 通过标签查找
soup.find_all(['p', 'div'])  # 查找p和div标签
soup.find_all('p', limit=3)  # 查找前三个p标签，返回标签

# 通过属性查找
soup.find_all(id='panda')  # 查找id为panda的标签，返回此标签全部内容例：<div id='panda'>内容</div>

tr = soup.find(attrs={'id': 'places_area__row'})
td = tr.find(attrs={'class': 'w2p_fw'})


# 通过正则配合内容查找
soup.find_all(text=re.compile('content$'))  # 查找标签内容以content结尾，以列表形式返回标签的文本内容。



################### css选择器
# 标签名查找
soup.select('p')  # 查找p标签

# 类名查找
soup.select('.p-class')  # 查找类名为p-class的标签

# id查找
soup.select('#panda')  # 查找id为panda的标签

# 组合查找
soup.select('p #panda')  # 查找p标签下id为panda的标签

# 属性查找
soup.select('p[class="p-class"]')  # 查找class='p-class'的p标签



'''
