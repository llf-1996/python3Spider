import json,math,time,pymongo,requests

#通过提交表单获得json数据
client=pymongo.MongoClient('localhost',27017)
mydb=client['mydb']
lagou=mydb['lagou']

headers={
    'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip,deflate,br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length':'25',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'JSESSIONID=ABAAABAABEEAAJA0BBB6FE124D323BDC4829DF925571AAD; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521970088; _ga=GA1.2.299899469.1521970088; user_trace_token=20180325172807-d38d40fd-300e-11e8-9d7d-525400f775ce; LGUID=20180325172807-d38d45b4-300e-11e8-9d7d-525400f775ce; index_location_city=%E5%85%A8%E5%9B%BD; LGSID=20180325184539-a874e880-3019-11e8-9d80-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3Dsug%26fromSearch%3Dtrue%26suginput%3Dpyth; TG-TRACK-CODE=index_search; ab_test_random_num=0; _putrc=370D01BAEF24F673123F89F2B170EADC; login=true; hasDeliver=0; gate_login_token=b6f6b92ab4eedec118b7b7c011904596ce5793ab7f2521c087327722c122ac54; _gat=1; unick=llf; witkey_login_authToken="Vo8lPXEFrE68fgY22YhTYamKuMuxx8c5J+PDJ6lBxur460izGrMNCAHL5yGPa1wByuLSNR1cIlj/uysDxWjz+JK6v0smRFOxhuE/BA7SkcU/WNxpDTPFEVD12/qGR5qdy8h+f9v1PDfOPJZislhA2Onffw4O1t1a7O/bmDnswmt4rucJXOpldXhUiavxhcCELWDotJ+bmNVwmAvQCptcy5e7czUcjiQC32Lco44BMYXrQ+AIOfEccJKHpj0vJ+ngq/27aqj1hWq8tEPFFjdnxMSfKgAnjbIEAX3F9CIW8BSiMHYmPBt7FDDY0CCVFICHr2dp5gQVGvhfbqg7VzvNsw=="; LGRID=20180325190051-c7eb4ed1-301b-11e8-b62d-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1521975652; SEARCH_ID=e38688eb34ff4f459495082655b72c72',
    'Host': 'www.lagou.com',
    'Origin': 'https://www.lagou.com',
    'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=sug&fromSearch=true&suginput=pyth',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token': 'None',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page(url,params):
    html=requests.post(url,data=params,headers=headers)
    json_data=json.loads(html.text)
    total_count=json_data['content']['positionResult']['totalCount']
    page_number=math.ceil(total_count/15) if math.ceil(total_count/15)<30 else 30

    get_info(url,page_number)


def get_info(url,page):
    for pn in range(1,page+1):
        params={
            'first':'false',
            'pn':str(pn),
            'kd':'Python'
        }
        try:
            html=requests.post(url,data=params,headers=headers)
            json_data=json.loads(html.text)
            results=json_data['content']['positionResult']['result']
            for result in results:
                infos={
                    'businessZones': result['businessZones'],
                    'city': result['city'],
                    'companyFullName': result['companyFullName'],
                    'companyLabelList': result['companyLabelList'],
                    'companySize': result['companySize'],
                    'district': result['district'],
                    'education': result['education'],
                    'explain': result['explain'],
                    'financeStage': result['financeStage'],
                    'firstType': result['firstType'],
                    'formatCreateTime': result['formatCreateTime'],
                    'gradeDescription': result['gradeDescription'],
                    'imState': result['imState'],
                    'industryField': result['industryField'],
                    'jobNature': result['jobNature'],
                    'positionAdvantage': result['positionAdvantage'],
                    'salary': result['salary'],
                    'secondType': result['secondType'],
                    'workYear': result['workYear']
                }
                print('------------------------------------------')
                print(infos)

                lagou.insert_one(infos)
            time.sleep(2)
        except requests.exceptions.ConnectionError:
            pass


if __name__ == "__main__":
    url='https://www.lagou.com/jobs/positionAjax.json'
    params={
        'first':'true',
        'pn':'1',
        'kd':'python'
    }
    get_page(url,params)




