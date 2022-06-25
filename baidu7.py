from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

import time


# 通过浏览器加载页面

# driver = webdriver.PhantomJS()
# options
option = webdriver.FirefoxOptions()
option.add_argument('-headless')
option.add_argument("--disable-gpu")


service = Service('C:/Program Files/Mozilla Firefox/geckodriver.exe')
driver = webdriver.Firefox(service=service, options=option)

# 打开URL界面
driver.get('https://www.baidu.com/')

# 截屏
# driver.save_screenshot('baidu.png')

# 找出要搜索的输入框
# driver.find_element_by_id('kw').send_keys('爹')
driver.find_element(By.ID, 'kw').send_keys('ma')

# 截屏
# driver.save_screenshot('baidu.png')

# 找出要搜索的提交
# driver.find_element_by_id('su').click()
driver.find_element(By.ID, 'su').click()
time.sleep(2)

# 截屏
driver.save_screenshot('baidu.png')




