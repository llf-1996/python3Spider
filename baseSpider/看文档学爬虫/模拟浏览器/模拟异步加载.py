'''
selenium爬取简书网
'''
#coding=utf-8
#简书网  /html/body/div[1]/div[1]/div[1]/div[1]/div/div/span[1]

from selenium import webdriver

driver=webdriver.PhantomJS()
driver.get('https://www.jianshu.com/p/3a7b1f47b29d')
include_title=[]
driver.implicitly_wait(100)

article=driver.find_element_by_xpath('//div[@class="article"]/h1').text
author=driver.find_element_by_xpath('//span[@class="name"]/a').text
data=driver.find_element_by_xpath('//span[@class="publish-time"]').text
word=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/div/div/span[2]').text
view=driver.find_element_by_xpath('//span[@class="views-count"]').text
comment=driver.find_element_by_xpath('//div[@class="meta"]/span[@class="comments-count"]').text
likes=driver.find_element_by_xpath('//div[@class="meta"]/span[5]').text
reward=driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/div/div/span[6]').text
includes=driver.find_elements_by_xpath('//div[@class="include-collection"]/a/div')

for i in includes:
    include_title.append(i.text)

print("标题:",article)
print("作者:",author)
print('时间：',data)
print(word)
print(view)
print(comment)
print('喜欢：',likes)
print('赞赏：',reward)
print('专题收入：',include_title)

