'''
PhantomJS是一个而基于WebKit的服务端JavaScript API,支持Web而不需要浏览器支持，
其快速、原生支持各种Web标准：Dom处理，CSS选择器，JSON等等。
PhantomJS可以用用于页面自动化、网络监测、网页截屏，以及无界面测试。
功能虽然不强大，但是用法简单的库。
安装：pip install selenium
'''

# coding=utf-8
from selenium import webdriver

# 当运行该命令时，会弹出一个空的浏览器窗口
# 可以到下面的地址下载chromedirver,其他浏览器也一样
# http://npm.taobao.org/mirrors/chromedriver/
driver = webdriver.Chrome(r"E:\myplugins\chromedriver.exe")

# 参数数字为像素点
print("设置浏览器宽480、高800显示")
driver.set_window_size(480, 400)

# 如果想在选定的浏览器中加载网页，可以调用get()方法：
driver.get('http://example.webscraping.com/places/default/search')

# 设置需要选取的元素，这里使用的是搜索文本框的ID.
# 此外,Selenium 也支持使用 css 选择器或 XPath 来选取元素。当找到搜索文本框之后，我们可以通过send_keys()方法输入内容，模拟键盘输入
driver.find_element_by_id('search_term').send_keys('.')
# 为了让所有结果可以在一次搜索后全部返回，我们希望把每页显示的数量
# 设置为1000。但是，由于 Selenium 的设计初衷是与浏览器交互，而不是修改
# 网页内容，因此这种想法并不容易实现。要想绕过这一限制，我们可以使用
# JavaScript 语句直接设置选项框的内容 。
js = "document.getElementById('page_size').options[1].text='1000'"
driver.execute_script(js)
# driver.find_element_by_id('search').click()
driver.find_element_by_id('search').click()

# 可以通过implicitlywait()方法设置超时时间。
driver.implicitly_wait(30)
# 我们设置了30秒的延时。如果我们要查找的元素没有出现，Selenium
# 至多等待30秒，然后就会抛出异常。要想选取国家链接，我们依然可以使用
# WebKit示例中用过的那个 css 选择器 。

links = driver.find_elements_by_css_selector('#results a')
countries = [link.text for link in links]
print(countries)
print(len(countries))
# 调用close()方法关闭浏览器
driver.close()
