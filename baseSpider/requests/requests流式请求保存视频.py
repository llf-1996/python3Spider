'''
requests高级用法：流式请求
stream=true, 下载视频
'''

import requests

res = requests.get('http://180.97.150.12/play/A16A0CA0EFC29C92D04B64E5DEEA7AFDFD46DAD7.mp4?token=REFERjFBNzEyN0ZDQ0UwQUY0N0MwRkQ3MTdCRUM3QzY0NjYzNjU0NV9td2ViXzE1NDM0MTUzOTk%3D&user_id=0&user_token=&vf=MCw0MjE5QQ%3D%3D&fudid=1532499691c99e1&app_code=mweb', stream=True)
content = res.iter_content()
with open('1.mp4', 'wb') as f:
    for i in content:
        if i:
            f.write(i)
print('下载完成')

