from selenium import webdriver
#需要下载chrome的driver插件，放在环境变量的目录下使之可以找到它，或者在下面webdriver.Chrome(executable_path="**driver.exe")中指定该文件的路径也可
driver = webdriver.Chrome()
driver.get("http://www.baidu.com")



print(driver.page_source)
driver.close()
