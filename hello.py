from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService

service = FirefoxService('C:/Program Files/Mozilla Firefox/geckodriver.exe')
option = webdriver.FirefoxOptions()
# 配置是否显示浏览器
# option.add_argument('-headless')

driver = webdriver.Firefox(service=service, options=option)
driver.get('https://www.baidu.com/')
driver.save_screenshot('baidu.png')
# 隐性等待
driver.implicitly_wait(0.5)
