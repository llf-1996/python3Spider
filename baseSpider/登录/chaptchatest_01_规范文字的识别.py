"""
__title__ = ''
__author__ = 'Thompson'
__mtime__ = '2018/7/26'
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
import pytesseract
from PIL import Image

image = Image.open('./images/tesseracttest.jpg')
# image = Image.open('./images/recaptcha.png')  # 带有背景的验证码无法识别
text = pytesseract.image_to_string(image)
print(text)


