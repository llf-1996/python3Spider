import os


def save(html, path):
    '''
    以文件形式保存数据
    :param html: 要保存的数据
    :param path: 要保存数据的路径
    :return:
    '''
    # 判断目录是否存在
    if not os.path.exists(os.path.split(path)[0]):
        # 目录不存在创建
        os.makedirs(os.path.split(path)[0])
    try:
        # 保存数据到文件
        with open(path, 'wb') as f:
            f.write(html.encode('utf8'))
        print('保存成功')
    except Exception as e:
        print('保存失败', e)


if __name__ == "__main__":
    html = '数据'  # 要保存的数据
    path = 'D:/a/b/1.txt'  # 设置路径，也可设为相对路径
    save(html, path)

