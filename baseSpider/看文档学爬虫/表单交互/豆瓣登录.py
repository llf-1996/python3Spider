#coding = "utf-8"

'''import requests
url='https://www.douban.com/accounts/login'
params={
    'source':'index_nav',
    'form_email':'2367746876@qq.com',
    'form_password':'l1515925742'
}
html=requests.post(url,params)
html=html.content.decode('utf-8')
print(html)
with open('douban.html','w',encoding='utf-8') as w:
    w.write(html)
'''

import requests
headers={
    'Cookies':'ll="118249";bid=L9YrthtYWJU;_pk_id.100001.8cb4=dffe28e9f10319fb.1521959494.1.1521961757.1521959494.;_pk_ses.100001.8cb4=*;ps=y;push_noty_num=0;push_doumail_num=0;ap=1'
}
url="https://www.douban.com"
html=requests.get(url,headers=headers)
print(html.text)

