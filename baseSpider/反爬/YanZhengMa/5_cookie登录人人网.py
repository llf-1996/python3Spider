"""
__title__ = ''
__author__ = 'llf'
__mtime__ = ''
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

# 获取一个有登录信息的 Cookie 模拟登陆，此cookie是登录后在浏览器中复制的
# 可以利用上面的例子模拟登陆后得到cookie值，保存即可。

from urllib import request
import chardet

# 1. 构建一个已经登录过的用户的 headers 信息
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # 重点：这个 Cookie 是保存了密码无需重复登录的用户的 Cookie，这个 Cookie 里记录了用户名，密码(通常经过 RAS 加密)
    "Cookie": "anonymid=jhsxb2breoia7; _r01_=1; ln_uact=17752558702; ln_hurl=http://head.xiaonei.com/photos/0/0/men_main.gif; _de=32B20555AD3784A6BF2D3D01B72FE013; depovince=HEN; jebe_key=bbeaa27f-d9ca-4b24-84bb-7c1a63164ca5%7C077a3e2b1c00096d5c13732ceee74ce5%7C1541980323171%7C1%7C1541980325116; jebecookies=654c5fe4-3bc0-45b1-ae8b-f4c5af05af15|||||; JSESSIONID=abcicW28vNhRu_pP2NgCw; ick_login=c56c89d3-bb9e-437f-8e1d-7390b4366391; p=33ac67acbedea32629d6ea941023948c2; first_login_flag=1; t=ba8110d960649ac08a341802353afc672; societyguester=ba8110d960649ac08a341802353afc672; id=966924492; xnsid=f9603ea4; ver=7.0; loginfrom=null; wp_fold=0",
}
# 2. 通过 headers 里的报头信息（主要是 Cookie 信息），构建 Request 对象
req = request.Request("http://www.renren.com/966924492/", headers=headers)
# 3. 直接访问 renren 主页，服务器会根据 headers 报头信息（主要是 Cookie 信息），判断这是一个已经登录的用户，并返回相应的页面
response = request.urlopen(req)
# 4. 打印响应内容
html = response.read()

# 判断编码并解码
charset = chardet.detect(html)['encoding']
print(charset)
print(html.decode(charset))
