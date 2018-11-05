from selenium import webdriver
import requests
from scrapy.selector import Selector
from fake_useragent import UserAgent
import time

ua = UserAgent()
headers = {
    "UserAgent": ua.random
}
driver = webdriver.Chrome()

driver.get("http://www.zhihu.com")

selector = Selector(text=driver.page_source)
html = driver.page_source
with open('zhihu.txt', 'w', encoding='utf8') as fs:
    fs.write(html)

driver.find_element_by_css_selector("div.SignContainer-switch>span").click()
# print(driver.page_source)
# driver.close()

print(driver.current_url)
response = requests.get(driver.current_url)

html = response.text
with open('zhihu1.txt', 'w', encoding='utf8') as fs:
    fs.write(html)

driver.implicitly_wait(5)
driver.find_element_by_name("username").clear()
driver.find_element_by_name("username").send_keys("15038712879")
time.sleep(2)
driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys("1515925742")
time.sleep(2)

try:
    # img[@class=Captcha-englishImg]/@src
    # captcha_url = selector.xpath("//img[@class='Captcha-chineseImg']/@src ")
    captcha_url = selector.xpath("div//img[@class='Captcha-englishImg']/@src").extract_first('')
    response = requests.get(captcha_url)
    image = response.content
    with open("image.png", "wb", encoding="utf8") as fp:
        fp.write(image)

    from PIL import Image

    im = Image.open('image.png')
    im.show()
    captcha = input("输入验证码：")
    driver.find_element_by_name("captcha").clear()
    driver.find_element_by_name("captcha").send_keys(captcha)
except:
    pass

# driver.find_element_by_class_name("SignFlow-submitButton").click()
# cookies = driver.get_cookies()
# print(cookies)

# time.sleep(5)
# driver.close()
'''
{'domain': '.zhihu.com',
 'httpOnly': False, 
 'name': 'd_c0',
  'path': '/',
   'secure': False, 
   'value': '"ACCvEquofg2PTgPI5cSvLSYSmOMYvL-V4r0=|1524618231"'
   }, 
   {'domain': '.zhihu.com',
    'httpOnly': False,
     'name': '_xsrf',
      'path': '/',
       'secure': False,
        'value': '308c014b-741d-4257-8b31-31924eb78c8c'}, 
        {'domain': 'www.zhihu.com',
         'httpOnly': True, 
         'name': 'aliyungf_tc',
          'path': '/',
           'secure':False, 
           'value': 'AQAAACLa0FlvDgMAW2XCeDNKlsgbBiaq'},
        {'domain': '.zhihu.com',
         'expiry': 1527210234.528358,
          'httpOnly': True,
           'name': 'capsion_ticket',
            'path': '/', 
            'secure': False, 
            'value': '"2|1:0|10:1524618233|14:capsion_ticket|44:ZmQ0NTJkMTU0Yjg4NGI4M2JkMTNkY2JmMzI2ZjE5OTM=|c49769a88a9e4bad85d5aa3974e1836a0eb13cafbe5c70f077e9ed0b1ea602ac"'}, 
        {'domain': '.zhihu.com',
         'expiry': 1587690234, 
         'httpOnly': False,
          'name': '_zap',
           'path': '/',
            'secure': False,
             'value': '1be8112f-8440-4a41-a01b-445c3b25827c'}

'''
