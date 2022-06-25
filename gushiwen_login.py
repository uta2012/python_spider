from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from lxml import etree
import time

from chaojiying import Chaojiying_Client


service = FirefoxService('C:/Program Files/Mozilla Firefox/geckodriver.exe')
option = webdriver.FirefoxOptions()
# 配置是否显示浏览器
# option.add_argument('-headless')

driver = webdriver.Firefox(service=service, options=option)
driver.get('https://www.chaojiying.com/user/login/')

# 截图
# driver.save_screenshot('baidu.png')

# 隐性等待
driver.implicitly_wait(0.5)

# 创建超级🦅对象
code_identify = Chaojiying_Client('2267176649', 'Leishangzhi2012', '935515')


code_pic = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/div/img').screenshot_as_base64

# 账号
driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[1]/input').send_keys('2267176649')
# 密码
driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[2]/input').send_keys('123456')
print(code_identify.PostPic_base64(code_pic, 1004))
driver.implicitly_wait(1)
# 验证码
driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[3]/input').send_keys(code_identify.PostPic_base64(code_pic, 1004)['pic_str'])

driver.implicitly_wait(0.5)

driver.find_element(By.XPATH, '/html/body/div[3]/div/div[3]/div[1]/form/p[4]/input').click()
