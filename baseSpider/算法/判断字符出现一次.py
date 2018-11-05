import re

__author__ = "llf"
'''
给定一个列表，判断其中所有的字符是不是都只出现过一次
'''
the_list = ["abc", "bcd", 'efg', 'fgh', 'ijk', 'jk']
the_str = str(the_list)
# 剔除数据
the_str = the_str.replace('[', '')
the_str = the_str.replace(']', '')
all = set(the_str)  # 所有不重复的元素
result1 = []
result2 = []
for i in all:
    res = the_str.count(i)
    if res == 1:
        result1.append(i)
print("count()结果：", result1)


for i in all:
    if i != '[' and i != ']':
        res = re.findall(i, the_str)
        if len(res) == 1:
            result2.append(i)
print("re.findall结果：", result2)
