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
import pytesseract
from PIL import Image
# img =Image.open('./images/recaptcha.png')
# img.show()
# print(pytesseract.image_to_string(img))

img =Image.open('./images/recaptcha.png')
img.show()
#可以看出，验证码文本一般都是黑色的，背景则会更加明亮，所以我们可以通过检查像素是否为黑色将文本分离出来，该处理过程又被称为阈值化。通过 Pillow 可以很容易地实现该处理过程。
gray = img.convert('L') #灰度化
gray.show()
# 二值化
bw = gray.point(lambda x: 0 if x < 1 else 255,'1')
bw.show()
print(pytesseract.image_to_string(bw))

