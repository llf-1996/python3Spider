'''
写一个方法，传入一个整型列表，计算其中不重复数字的个数并返回
'''


def fun(a):
    '''
    获取不重复的元素
    :param a:
    :return:
    '''
    aa = set(a)  # 不重复的数据集
    res = []  # 存放结果集
    for i in aa:
        if a.count(i) == 1:  # 元素出现次数为1
            res.append(i)
    return res


if __name__ == "__main__":
    a = [1, 2, 3, 5, 8, 5, 4, 1, 10, 11, 5]
    res = fun(a)
    print(res)

