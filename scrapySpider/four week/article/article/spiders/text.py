'''
list=['IT技术', ' 1 评论 ', 'Redis', '数据库']
list =[element for element in list if not element.strip().endswith("评论")]
li='-'.join(list)
print(li)
print(type(list))
print(len(list))
print(type(str(list)))


'''


'''
class Dog(object):
    def __init__(self):
        print("----init方法-----")

    def __del__(self):
        print("----del方法-----")

    def __str__(self):
        print("----str方法-----")
        return "对象的描述信息"

    def __new__(cls):#cls此时是Dog指向的那个类对象

        #print(id(cls))

        print("----new方法-----")
        return object.__new__(cls)


#print(id(Dog))

xtq = Dog()

'''

'''
class A(object):  # A must be new-style class
    def __init__(self):
        print("enter A")
        print("leave A")
class B(A):  # A --> C
    def __init__(self):
        print("enter B")
        #super(B, self).__init__()
        super().__init__()
        print("leave B")

b=B()

'''
'''
dict = {'Name': 'Runoob', 'Age': 7}
print(dict.get("name"))

'''

'''
def foo(x):
    print("executing foo(%s)" % (x))


class A(object):
    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)

a = A()
print(a.foo(1))

'''
def a():
    aa='1'
    bb=2
    return aa,bb
f=a()

print(type(f))
c,d=a()
print(type(c))
print(c,d)
















