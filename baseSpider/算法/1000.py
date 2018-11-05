'''
如果 a+b+c=1000，且 a^2+b^2=c^2（a,b,c 为自然数），如何求出所有a、b、c可能的组合?
'''
__author__ = "llf"

for a in range(1000):
    for b in range(1000):
        c = 1000 - a - b
        if c >= a and c >= b and a ** 2 + b ** 2 == c ** 2:
            print("结果：", a, b, c)

'''
结果： 0 500 500
结果： 200 375 425
结果： 375 200 425
结果： 500 0 500
'''