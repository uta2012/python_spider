from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from lxml import etree
import time


class huyazhibo:
    def __init__(self):
        self.service = Service('C:/Program Files/Mozilla Firefox/geckodriver.exe')
        self.option = webdriver.FirefoxOptions()
        self.option.add_argument('-headless')
        self.option.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(service=self.service, options=self.option)
        self.room_count = 0
        self.hot_count = 0

    def run(self):
        # 打开url页面
        # self.driver.get('https://www.huya.com/l')

        # 爬取相关内容
        content = self.driver.page_source
        content2 = etree.HTML(content)
        # 获取房间所有信息
        rooms = content2.xpath('//ul[@id="js-live-list"]/li[@class="game-live-item"]')
        for room in rooms:
            # 获取房间名称
            room_name = ''
            tmp = room.xpath('./a[@class="title"]/text()')
            if len(tmp) > 0:
                room_name = tmp[0]
            # 获取房间人气
            room_hot = ''
            tmp = room.xpath('./span[@class="txt"]/span[@class="num"]/i[@class="js-num"]/text()')
            if len(tmp) > 0:
                room_hot = tmp[0]

            print('房间人气：%s 房价名称：%s ' % (room_hot, room_name))

            # 计算总房价数
            self.room_count += 1
            #计算总人气数
            if room_hot[-1] == '万':
                room_hot = room_hot[:-1]
                room_hot = int(float(room_hot) * 10000)
                self.hot_count += room_hot
            else:
                self.hot_count += int(room_hot)

        print('当前直播数量：%d 当前直播热度：%d' % (self.room_count, self.hot_count))

    def test(self):
        # self.driver.get('https://www.huya.com/l')

        page = 0
        while True:
            page += 1
            time.sleep(1)
            # 尝试查找 class = laypage_next 下一页
            # find('laypage_next') 有东西返回数量，没有返回-1
            ret = self.driver.page_source.find('aria-disabled="false"')
            if ret > -1:
                self.run()
                print('第%d页' % page)
            else:
                self.run()
                print('第%d页，这是最后一页' % page)
                break
            self.driver.find_element(By.CLASS_NAME, 'laypage_next').click()





if __name__ == '__main__':
    huya = huyazhibo()
    # huya.run()
    huya.test()
