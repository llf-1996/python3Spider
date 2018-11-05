'''
给定一个数组 strs，其中的数据都是字符串，给定两个字符串 str1，str2。如果这两个字符串都在 strs数组中，就返回它们之间的最小距离；如果其中任何一个不在里面，则返回 -1；如果两个字符串相等，则返回 0。
'''
import re


def fun(source_str, str1, str2):
    '''
    验证数据
    :param source_str:
    :param str1:
    :param str2:
    :return:
    '''
    the_source_str = str(source_str)
    res1 = re.findall(str1, the_source_str)
    res2 = re.findall(str2, the_source_str)
    # 均存在
    if res1 and res2:
        if str1 == str2:
            if len(res1) >= 2:
                return 0  # 字符相同且均存在
        else:
            index1 = source_str.index(str1)
            index2 = source_str.index(str2)
            res = abs(index2 - index1)
            return res  # 字符不同且均存在
    # 只存在一个
    if res1 or res2:
        return -1
    # 不存在
    if not res1 and not res2:
        return "不存在"


the_str = ['a', 'b', 'c', 'cc']
str1 = 'a'
str2 = 'a'
res = fun(the_str, str1, str2)
print(res)
