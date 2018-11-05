'''
计算斐波那契数列。具体什么是斐波那契数列，那就是0，1，1，2，3，5，8，13，21，34，55，89，144，233。
'''


def fib(max):
    '''
    斐波拉契数列
    :param max:
    :return:
    '''
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a + b
        n = n + 1
    return 'done'


if __name__ == "__main__":
    res = []
    for n in fib(6):
        res.append(n)
    print(res)

