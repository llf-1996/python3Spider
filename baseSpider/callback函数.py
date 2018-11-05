'''
callback函数从大到小排序
'''

a = [{'id': 1}, {'id': 2}, {'id': 0}]


def pop(callback):
    '''
    冒泡排序
    :param callback:
    :return:
    '''
    for i in range(0, len(a)):
        for j in range(0, len(a) - i - 1):
            if callback(a[j], a[j + 1]):
                a[j], a[j + 1] = a[j + 1], a[j]


def comp(a1, a2):
    '''
    比较回调函数
    :param a1:
    :param a2:
    :return:
    '''
    return a1['id'] < a2['id']


pop(comp)
print(a)
