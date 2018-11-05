'''
pyQuery强大又灵活的网页解析库，熟悉jQuery的语法可以非常快的使用pyquery
 css选择器
'''

from pyquery import PyQuery as pq

html = '''
<div class="wrap">
    <div class="container">
        <ul class="list">
             <li class="item-0"><a href="link1.html">first item</a></li>
             <li class="item-1 active"><a href="link2.html">second item</a></li>
             <li class="item-inactive"><a href="link3.html">third item</a></li>
             <li class="item-1"><a href="link4.html">fourth item</a></li>
             <li class=item-0><a href="link5.html">fifth item</a>
         </ul>
     </div>
</div>
'''

############# 初始化
# 字符串初始化
print('############' * 10)
doc = pq(html)
print(doc('li'))  # 标签通过标签名，也可通过#id或.class的方式获取内容   自动修复

# 输出如下：
'''
<li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0&quot;"><a href="link5.html">fifth item</a>
     </li>
'''

# url初始化
print('############' * 10)

doc1 = pq(url='http://www.baidu.com')
print(doc1('head'))

# 文件初始化
print('############' * 10)
doc2 = pq(filename='demo.html')
print(doc('.item-inactive'))

########## 查找元素
# 查找子元素
doc = pq(html)
items = doc('ul')
print(type(items))
print(items)
lis = items.find('li')  # 子孙元素
print(type(lis))
print(lis)

# lis = items.children([.class])  # 子元素

# 父元素
doc = pq(html)
items = doc('.item-inactive')
# container = items.parent()  # 获取父元素
containers = items.parents()  # 获取所有祖先节点
print(containers)
# containers = items.parents().items()  # 生成器   获取所有祖先节点并遍历输出，
# for i in containers:
#     print(i)

# 兄弟元素
print('#######兄弟元素##################################')
doc = pq(html)
li = doc('.list .item-1.active')  # 获取li元素
print(li.siblings())

####################### 遍历
print('##################遍历')
# 单个元素
doc = pq(html)
li = doc('.list .item-1.active')  # 获取li元素
print(li.siblings())

print('#### 多个元素')
# 多个元素
doc = pq(html)
lis = doc('li').items()  # 获取li元素
for li in lis:
    print(li)

print("################### 获取信息")
print('# 获取属性')
doc = pq(html)
a = doc('.item-1.active a')
print(a)
print(a.attr('href'))
print(a.attr.href)

print('# 获取文本,不包含标签')
doc = pq(html)
a = doc('.item-1.active a')
print(a)
print(a.text())

print('# 获取HTML')
doc = pq(html)
a = doc('.item-1.active')
print(a)
print(a.html())

print("############################# DOM操作")
print('# addClass、removeClass')
doc = pq(html)
li = doc('.item-1.active')
print(li)
li.remove_class('active')  # remove_class
print(li)
li.add_class('active')  # 添加class  也可使用addClass()结果一样
print(li)

print("# 添加或修改属性和添加样式  attr、css")
doc = pq(html)
li = doc('.item-1.active')
print(li)
li.attr('name', 'link')  # 添加属性
print('添加name属性：', li)
li.css('font-size', '14px')  # 添加样式
print('添加样式：', li)

print("# 删除标签 remove")
html1 = '''
<div class="wrap">
hello,world
<p>This is a paragraph.</p>
</div>
'''
doc = pq(html1)
wrap = doc('.wrap')
print(wrap.text())
wrap('p').remove('p')  # 移除p标签
print('remove后：', wrap.text())
print('原标签：', wrap)

print('########################### 伪类选择器')
doc = pq(html)
li = doc('li:first-child')
print('第一个li: ', li)
li = doc('li:last-child')
print('最后一个li：', li)
li = doc('li:nth-child(2)')
print('第二个li：', li)
li = doc('li:gt(2)')  # 索引大于2的li  索引从0开始
print('索引大于2的li：', li)
li = doc('li:nth-child(2n)')
print('获取第偶数个的li：', li)
li = doc('li:contains(second)')
print('包含指定文本的li：', li)




