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
'''
selenium：多窗口页和frame子窗口切换

# 跳出当前iframe
self.driver.switch_to.parent_frame()

# 返回最外层iframe
self.driver.switch_to.default_content()

'''

from selenium import webdriver

driver = webdriver.Chrome(r"E:\myplugins\chromedriver.exe")
driver.get('http://datamining.comratings.com/exam')

driver.implicitly_wait(2)

handle = driver.current_window_handle
print("获取到当前的handle：%s" % handle)

#
# 获取全部的handle句柄
handles = driver.window_handles
print(handles)
print(type(handles))    # 结果为list类型
# 切换到最后一个窗口
driver.switch_to.window(handles[-1])
handle2 = driver.current_window_handle
print("获取到当前的handle：%s" % handle2)
print(driver.page_source)
handles3 = driver.window_handles
print(handles3)

driver.implicitly_wait(2)
# 进入frame子窗口
a = driver.find_element_by_xpath("//iframe[@frameborder='no']")
driver.switch_to.frame(a)
print('###########', driver.page_source)

driver.close()


