"""
__title__ = ''
__author__ = 'llf'
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
selenium和pil获取百度首页的百度logo
'''

from selenium import webdriver
from PIL import Image

browser = webdriver.Chrome(r"E:/myplugins/2.42/chromedriver.exe")
browser.get('https://www.baidu.com')
browser.save_screenshot('./images/baidu.png')
element = browser.find_element_by_xpath('//div[@id="lg"]/img[1]')
# location办法可能会有偏移，但是每次都会锁定了验证码的位置，所以稍微修正一下location的定位，后面都管用，或者修改比例
left = element.location['x']  # 验证码图片左上角横坐标
top = element.location['y']  # 验证码图片左上角纵坐标
right = left + element.size['width']  # 验证码图片右下角横坐标
bottom = top + element.size['height']  # 验证码图片右下角纵坐标
print(left, top, right, bottom)
# 截取图片
im = Image.open('./images/baidu.png')
im_crop = im.crop((left, top, right, bottom))  # 这个im_crop就是从整个页面截图中再截出来的验证码的图片
im_crop.save('./images/logo.png')
browser.quit()
