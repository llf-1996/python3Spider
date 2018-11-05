'''
bs4解析网页
'''

from bs4 import BeautifulSoup

html = '''
<html><head><title id='id_title' class='class_title1 class_title2'>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<div><!-- comment test --></div>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class=story>...</p>
'''
soup = BeautifulSoup(html, 'lxml')

# print(soup.prettify())  # prettify()补全网页
print(soup)  # prettify()补全网页



# tag
print('title type:', type(soup.title))
print('title name:', soup.title.name)  # title标签的名称  title
print('title attr:', soup.title.attrs)  # title标签的所有属性

# navigablestring
print('soup.p.string type:', type(soup.p.string))  # 标签内的文字
print('soup.p.string contents:', soup.p.string)

print("soup.b.parent:", soup.b.parent)
print("soup.b.parents:", soup.b.parents)
for i in soup.b.parents:
    print("parents name:", i.name)

print("soup.p.next_sibling:", repr(soup.p.next_sibling))
# soup.p.previous_sibling
print("soup.p.next_siblings:", list(soup.p.next_siblings))
# 前后
print("soup.p.next_element:", soup.p.next_element)
print("soup.p.next_elements type:", type(soup.p.next_elements))
for i in soup.p.next_elements:
    print("soup.p.next_element:", repr(i))


