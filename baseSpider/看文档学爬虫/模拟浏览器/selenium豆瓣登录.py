'''
selenium、chromdriver模拟浏览器豆瓣登录
'''
from selenium import webdriver

driver = webdriver.Chrome(r"E:\myplugins\chromedriver.exe")
driver.get('https://www.douban.com/')
driver.implicitly_wait(5)
driver.find_element_by_id('form_email').clear()
driver.find_element_by_id('form_email').send_keys('2367746876@qq.com')
driver.find_element_by_id('form_password').clear()
driver.find_element_by_id('form_password').send_keys('l1515925742')
driver.find_element_by_id('form_password').submit()
# driver.find_element_by_class_name('bn-submit').click()
print(driver.page_source)
# print(type(driver.page_source))  # <class 'str'>


