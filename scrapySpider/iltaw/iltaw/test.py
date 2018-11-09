from lxml import etree

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
html = etree.HTML(text)
nodeList = html.xpath('//ul')  # 第一次匹配ul
# print('nodelist：', nodeList)

# 二次匹配ul中的li
for i in nodeList:
    #### 错误内容
    # print(type(i))
    # print(etree.tostring(i))  # 输出li的内容
    i = i.xpath('/ul/li/a/text()')  # 此处并不是从遍历的li中匹配，而是从html中匹配的
    print(i)

    # ##### 解决方法：重新解析内容并匹配
    # i = etree.tostring(i)  # 将etree对象转换为字节
    # # print('tostring: ', i)
    # i = etree.HTML(i)  # 解析
    # content = i.xpath('//li/a/text()')
    # print('结果：', content)
