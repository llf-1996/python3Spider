from selenium import webdriver
import time
'''
#登录开源中国社区


browser = webdriver.Chrome(executable_path="C:\Program Files\Python36\chromedriver.exe")
browser.get("https://www.oschina.net/blog")
time.sleep(5)
for i in range(3):
    time.sleep(1)
    #用Javascript代码来进行鼠标滚动，  用来获取页面是动态加载的
    browser.execute_script("window.scrollTo(0,document.body.scrollHeight);"
                           "var lenOfPage=document.body.scrollHeight;"
                           "return lenOfPage;")

'''
'''
#设置Chrome不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(executable_path="C:\Program Files\Python36\chromedriver.exe",chrome_options=chrome_opt)
browser.get("https://www.taobao.com")
'''

'''
#使用phantomjs

browser = webdriver.PhantomJS(executable_path="C:/Program Files/Python36/phantomjs.exe")
browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.6.5f8c442byyrjT7"
            "&id=564739811420&cm_id=140105335569ed55e27b&abbucket=15")
print(browser.page_source)
browser.quit()
'''









