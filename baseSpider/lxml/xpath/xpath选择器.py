from lxml import etree

xml = '''
<bookstore>
​    <book id='mashang'>
ma
        <title lang="eng">Harry Potter</title>
         <price>29.99</price>
    </book>
   ​  <book id='xiami'>
          <title lang="eng">Learning XML</title>
           <price>39.95</price>
            <p>书店
     </book>
</bookstore>
'''


html = etree.HTML(xml)
nodeList = html.xpath('//book[contains(text(), "ma")]')
print(type(nodeList))  # <class 'list'>
print(dir(nodeList))
print(nodeList)

# print(len(nodeList))

# result = etree.tostring(html)
# print(result.decode('utf8'))
'''

'''

from lxml import etree

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)
nodeList = html.xpath('//a[contains(text(), "first")]/text()')
print(nodeList)
