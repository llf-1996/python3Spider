'''
css选择器
'''

import lxml.html
import requests


def brokenHtml():
    '''
    lxml页面补全
    :return:
    '''
    broben_html = "<ul class=country> <li>Area <li>Population</ul>"
    tree = lxml.html.fromstring(broben_html)
    return lxml.html.tostring(tree, pretty_print=True).decode('utf8')


# css选择器，筛选结点
def css():
    '''
    css筛选节点
    :return:
    '''
    html = requests.get("http://example.webscraping.com/places/default/view/Ethiopia-71")
    tree = lxml.html.fromstring(html.text)  # 获取tree对象
    # td = tree.cssselect('tr#places_area__row > td.w2p_fw ')[0]
    td = tree.cssselect('tr#places_phone__row>td[class=w2p_fl]>label[class=readonly]')[0]
    print(td)
    print('td.text: ', td.text)
    area = td.text_content()
    print('td.text_content()', area)


css()
