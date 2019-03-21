from selenium import webdriver


def get_id(name):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.implicitly_wait(10)
    driver.get('http://mainsearch-test.tigerobo.com/?query={}'.format(name))

    try:
        driver.find_element_by_partial_link_text('查看更多项目信息').click()
        url = driver.current_url
        # print(driver.current_url)
        # print('aa')
        url = url.replace('http://mainsearch-test.tigerobo.com/?', '')
        driver.close()
        return url
    except Exception as e:
        print(e)
        return None


def get_info(name_list):
    info_dict = dict()
    for name in name_list:
        res = get_id(name)
        info_dict[name] = res
    return info_dict


if __name__ == '__main__':
    res = get_info(['晶晨半导体'])
    print(res)

