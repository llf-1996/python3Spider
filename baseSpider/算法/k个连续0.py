'''
给定字符串str 和一个整数k。如果str中恰好出现了连续的k个0，则将k个0删除。 比如，给定字符串str = “0000fw300001203h000ui0000re3_0000”，k=4。返回的结果为“fw31203h000uire3_”。
'''

the_str = '0000fw300001203h000ui0000re3_0000'
k = 4


def fun(source_str, count):
    '''
    剔除元素
    :param source_str:
    :param count:
    :return:
    '''
    rep = '0'*count
    the_str = source_str.replace(rep, '')
    return the_str


res = fun(the_str, k)
print("结果：", res)
