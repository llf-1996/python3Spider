import urllib.request

url = "https://www.baidu.com/img/bd_logo1.png"
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
data = response.read()
print("============================")
print(response.geturl())
print("============================")
print(response.info())
print("============================")
print(response.getcode())

'''
with open("baidu.png","wb") as f:
    f.write(data)
'''
