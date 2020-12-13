# -*- coding: utf-8 -*-
# time: 2020-11-17
import random

import requests
import execjs

from config import URL, TOKEN, COOKIE, SIMPLE_MEANS_FLAG, TRIGGER_TYPE, USER_AGENT, REFERER


def get_sign(word):
    '''
    获取sign
    替换sign.js文件里的window[l]为"320305.131321201"
    计算方式：
    浏览器打开百度翻译标签页的检查元素在控制台执行
    l=""+String.fromCharCode(103)+String.fromCharCode(116)+String.fromCharCode(107);  // gtk
    window[l]
    '''

    # from selenium import webdriver
    # browser = webdriver.Chrome(executable_path='chromedriver.exe')
    # with open('eleme.js', 'r') as f:
    #     js = f.read()
    # print(browser.execute_script(js))

    with open('./sign.js', encoding='utf-8') as f:
        js = f.read()
    et = execjs.compile(js)
    sign = et.call('e', word)
    return sign


def to_translate(trans_from, trans_to, word):
    sign = get_sign(word)
    data={
        "from": trans_from,
        "to": trans_to,
        "query": word,
        # 可选
        "transtype": random.choice(TRIGGER_TYPE),
        # 可选
        "simple_means_flag": SIMPLE_MEANS_FLAG,
        # 必须
        "sign": sign,
        # 必须
        "token": TOKEN, # 通过查看浏览器的network对应请求获取
        # 可选
        "domain":"common"
    }
    headers={
        # 可选
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        # 必须
        "cookie": COOKIE,
        # 可选 通过查看浏览器的network对应请求获取
        "referer": REFERER,
        # 可选
        "user-agent": USER_AGENT
    }
    translate_url = '{}?from={}&to={}'.format(URL, trans_from, trans_to)
    rs=requests.post(translate_url, headers=headers, data=data)
    # print(rs.json())
    if rs.status_code == 200:
        datas = rs.json()['trans_result']['data']
        result = datas[0]['dst']
    else:
        result = None
    return result
