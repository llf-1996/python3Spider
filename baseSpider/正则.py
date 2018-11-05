import re

re.match(r'^\d{3}\-\d{3,8}$', '010-12345')
re.match(r'^\d{3}\-\d{3,8}$', '010 12345')
m = re.findall(r'\d{3}', '010-456123')
print("findall: ", m)

m = re.match(r'^(\d+?)(0*)$', '102300')
print("groups:", m.groups())

str = "th is string example....wow!!! th was really string"
print(str.replace("is", "123"))

