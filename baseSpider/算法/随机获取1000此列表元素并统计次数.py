'''
随机获取一个字符串列表中的字符串，求获取一千次的情况下，各字符串被随机到的次数。
'''

__author__ = 'llf'

import random
from collections import Counter

c = Counter()
ll = ['a', 'b']

for i in range(1000):
    a = random.choice(ll)
    c[a] = c[a] + 1

print('结果：', type(c), dir(c), c)

'''
<class 'collections.Counter'> 
[
'clear', 'copy', 'elements', 'fromkeys', 'get', 'items', 
'keys', 'most_common', 'pop', 'popitem', 'setdefault', 
'subtract', 'update', 'values'
] 
'''

