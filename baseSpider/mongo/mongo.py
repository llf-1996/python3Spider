#coding="utf-8"
from pymongo import MongoClient
client=MongoClient()
#print(client)
hello_db=client.hello  # hello数据库对象
user_collection=hello_db.user  # user集合对象，即user表
#print(user_collection)

user={
    "name":"py_xujunhao",
    "sex":"py_male",
    "age":18
}
#user_id=user_collection.insert(user)
#print(user_id)


'''
re=user_collection.find_one()
print(re)
re=user_collection.find({"name":"py_xujunhao"})
for i in re:
    print(i)
num=user_collection.find({"name":"py_xujunhao"}).count()
print(num)
'''


'''
#修改数据
user1={"name":"mike"}
user2={"$set":{"name":"llf"}}
res=user_collection.update_many(user1,user2)
re=user_collection.find()
for i in re:
    print(i)
'''

'''
#删除数据
user3={"name":"llf"}
res=user_collection.remove(user3)
print(res)

'''
