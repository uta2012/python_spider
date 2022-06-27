from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from lxml import etree
import time


class BilibiliSpider:
    def __init__(self, url):
        self.url = url
        self.service = FirefoxService('C:/Program Files/Mozilla Firefox/geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        # self.options.add_argument('-headless')
        # self.options.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

        # bilibili链接
        self.driver.get(url)
        self.video_count = 0

    def get_name(self):
        content = self.driver.page_source
        content.replace('<!--', '')
        content.replace('-->', '')
        print(content)

        content2 = etree.HTML(content)
        videos = content2.xpath('//div[@class="video-list row"]//div[@class="bili-video-card__info--right"]')
        print(videos)

        for video in videos:
            print(video)

    def driver_quit(self, t):
        time.sleep(t)
        self.driver.quit()



if __name__ == '__main__':
    url = 'https://search.bilibili.com/all?keyword=%E6%B5%8B%E8%AF%95&from_source=webtop_search&spm_id_from=333.1007'
    bilibili = BilibiliSpider(url)
    bilibili.get_name()
    bilibili.driver_quit(5)


