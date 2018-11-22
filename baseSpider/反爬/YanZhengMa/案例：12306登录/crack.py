'''
利用超级鹰打码平台进行12306验证码的识别
'''

import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from chaojiying import Chaojiying

# 12306账号和密码
EMAIL = 'username'  # 输入账号
PASSWORD = 'password'  # 输入密码
# 超级鹰账号和密码及soft_id
CHAOJIYING_USERNAME = '***'  # 输入用户名
CHAOJIYING_PASSWORD = '***'  # 输入密码
CHAOJIYING_SOFT_ID = '***'  # 输入soft_id,在超级鹰中自己创建
CHAOJIYING_KIND = 9004  # 验证码类型


class CrackTouClick():
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/login/init'
        self.browser = webdriver.Chrome(r"E:\myplugins\chromedriver.exe")
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.password = PASSWORD
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)
    
    def __del__(self):
        print('close')
        self.browser.close()
    
    def open(self):
        """
        打开网页输入用户名密码
        :return: None
        """
        self.browser.get(self.url)
        print(self.browser.page_source)
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email.send_keys(self.email)
        password.send_keys(self.password)
    
    def get_touclick_button(self):
        """
        获取初始验证按钮element_to_be_clickable
        :return:
        touclick-bgimg touclick-reload touclick-reload-normal
        """
        button = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'touclick-reload')))
        return button
    
    def get_touclick_element(self):
        """
        获取验证图片对象
        :return: 图片对象
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'touclick-image')))
        return element
    
    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        element = self.get_touclick_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (left,top,right, bottom)
    
    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        left, top, right, bottom = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha
    
    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result: 识别结果
        :return: 转化后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations
    
    def touch_click_words(self, locations):
        """
        点击验证图片
        :param locations: 点击位置
        :return: None
        """
        for location in locations:
            print(location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0],
                                                                   location[1]).click().perform()
            time.sleep(1)
    
    def touch_click_verify(self):
        """
        点击验证按钮
        :return: None
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn200s')))
        button.click()
    
    def login(self):
        """
        登录
        :return: None
        """
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginSub')))
        submit.click()
        time.sleep(10)
        print('登录成功')
    
    def crack(self):
        """
        破解入口
        :return: None
        """
        self.open()
        time.sleep(2)
        # 点击验证码刷新按钮
        button = self.get_touclick_button()
        button.click()
        time.sleep(2)
        # 获取验证码图片
        image = self.get_touclick_image("./images/12306.png")
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')
        # 利用超级鹰识别验证码
        result = self.chaojiying.post_pic(bytes_array.getvalue(), CHAOJIYING_KIND)
        print(result)
        locations = self.get_points(result)
        self.touch_click_words(locations)
        self.touch_click_verify()
        # 判定是否成功
        elem = self.wait.until(
             #EC.text_to_be_present_in_element((By.CLASS_NAME, 'touclick-hod-note'), '验证成功'))
            EC.presence_of_element_located((By.ID, 'error_msgmypasscode1')))

        print(elem.text)
        
        #失败后重试
        if len(elem.text)==0:
            print('success!')
            #self.login()

        else:
            print('fail!')
            #self.crack()


if __name__ == '__main__':
    crack = CrackTouClick()
    crack.crack()
