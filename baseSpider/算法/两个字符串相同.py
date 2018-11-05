'''
给定两个字符串，str1，str2，判断两个字符串中出现的字符是否全部种类一样，数量一样。
例如：
str1 = “apple”, str2 = “paple”, 返回 True;
str1 = “pear”, str2 = “bears”, 返回 False。

ps: is 与 == 区别：
is 用于判断两个变量引用对象是否为同一个， == 用于判断引用变量的值是否相等。
'''

str1 = 'apple'
str2 = 'apple'
if str1 == str2:
    print('true')
else:
    print('false')


'''
import hashlib
>>> a = 'adfd'
>>> b = 'adfd'
>>> c = 'addf'
>>> m = hashlib.md5(a.encode('utf-8'))
>>>
>>> m.hexdigest()
'84f57b4d03744d0bf803a1c9736c2b46'
>>>
>>> m = hashlib.md5(b.encode('utf-8'))
>>> m.hexdigest()
'84f57b4d03744d0bf803a1c9736c2b46'
>>> m = hashlib.md5(c.encode('utf-8'))
>>> m.hexdigest()
'240a8254415e3c29e645fb3fb4343bc0'
>>>
'''
