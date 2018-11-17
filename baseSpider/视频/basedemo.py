'''
保存视频
'''
import requests

response = requests.get('http://180.97.150.12/play/A16A0CA0EFC29C92D04B64E5DEEA7AFDFD46DAD7.mp4?token=NUQ4Q0EyQUY5QkMxRkRFRjdDRjc0NTg3NDVFOTlDNjg5NzI4QzcxM19td2ViXzE1NDIwMjU4OTY%3D&user_id=0&user_token=&vf=MCw0MjE5QQ%3D%3D&fudid=1532499691c99e1&app_code=mweb')
movie = response.content
with open('1.mp4', 'wb') as f:
    f.write(movie)
    print('保存成功')

