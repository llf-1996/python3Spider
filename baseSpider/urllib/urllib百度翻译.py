import urllib.request
import urllib.parse
import json

while True:
    content = input('请输入要翻译的内容(输入q!结束)：')
    if content == 'q!':
        break
    data = {}
    if ord(content[0]) in range(97, 122) or ord(content[0]) in range(65, 90):  # 是否是字母/英文
        data['from'] = 'en'
        data['to'] = 'zh'
    else:  # 中文
        data['from'] = 'zh'
        data['to'] = 'en'
    data['query'] = content
    data['transtype'] = 'translang'
    data['simple_means_flag'] = '3'
    data = urllib.parse.urlencode(data).encode('utf-8')

    head = {}
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3067.6 Safari/537.36'

    url = 'http://fanyi.baidu.com/v2transapi'
    req = urllib.request.Request(url, data, head)
    response = urllib.request.urlopen(req)
    html = response.read().decode('utf-8')

    print(html)
'''

    target = json.loads(html)

    print('翻译结果是：%s'%(target['trans_result']['data'][0]['dst']))

'''
