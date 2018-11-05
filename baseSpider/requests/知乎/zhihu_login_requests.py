'''
知乎登录
'''

import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
from fake_useragent import UserAgent

ua = UserAgent()
header = {
    "HOST": "www.zhihu.com",
    "User-Agent": ua.random
}
session = requests.session()
session.cookies = cookielib.LWPCookieJar()  # 实例化后可以调用直接save方法# 保存cookie


# 自动加载cookie
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("cookie未能加载")


def get_xsrf():
    response = session.get("https://www.zhihu.com", headers=header)
    # print(response.text)
    html = response.text
    match_obj = re.match('.*name="_xsrf" value="(.*?)"', html)
    match_xsrf = match_obj.group(1)
    if match_obj:
        # print(match_xsrf)
        return match_xsrf
    else:
        return ''


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    print("ok")


def zhihu_login(account, password):
    # 知乎登录
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }
        response = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()  # 自动将cookie保存在当前目录下的名为cookies.txt文件中


if __name__ == "__main__":
    print("是否已保存cookie：\n是：1    否：0")
    a = input("请输入：")
    if a == "0":
        user = input("用户名；")  # 设置用户名
        passwd = input("密码：")  # 设置密码
        zhihu_login(user, passwd)
    elif a == "1":
        get_index()
    else:
        print("输入错误")
