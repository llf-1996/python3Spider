class Person:
    '''
    person类
    '''
    num = 20  # 类属性

    def __init__(self, name, age):
        '''
        初始化
        :param name: 姓名
        :param age: 年龄
        '''
        self.name = name  # 类属性
        self.age = age

    def info(self):
        '''
        输出信息
        :return:
        '''
        print("name:", self.name)
        print("age:", self.age)
        print("类属性num:", self.num)


person = Person('tom', 5)
person.sex = '男'  # 定义实例属性
print('实例属性：', person.sex)
person.info()
