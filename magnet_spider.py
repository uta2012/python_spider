import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from lxml import etree
import time
import openpyxl
import pandas as pd


class MagnetSpider:
    def __init__(self, url):
        self.url = url
        self.service = FirefoxService('C:/Program Files/Mozilla Firefox/geckodriver.exe')
        self.options = webdriver.FirefoxOptions()
        #self.options.add_argument('-headless')
        #self.options.add_argument("--disable-gpu")
        self.driver = webdriver.Firefox(service=self.service, options=self.options)


        # self.driver.get(url)
        # self.video_count = 0

    # 获取演员链接。返回字典 演员:链接
    def get_actresses(self, url):
        self.driver.get(url)
        content = self.driver.page_source
        content.replace('<!--', '')
        content.replace('-->', '')
        # print(content)

        content2 = etree.HTML(content)
        actresses = content2.xpath('//div[@class="actresses"]/a/p/text()')
        # print(actresses)

        # 获取所有a标签的href属性
        resp = requests.get(self.url)
        html = etree.HTML(resp.text)
        # 获取所有a标签的href属性
        linklist = html.xpath('//div[@class="actresses"]/a/@href')

        for i in range(len(linklist)):
            linklist[i] = 'https://javtxt.net' + linklist[i]

        # print(linklist)

        actresses_and_linklist = dict(map(lambda a, b: [a, b], actresses, linklist))

        # for actress, link in actresses_and_linklist.items():
        #     print(actress, link)

        return actresses_and_linklist

    # 下载某个演员视频列表 返回字典 {number: [link, description]}
    def get_video_message(self, url):
        self.driver.get(url)
        content = self.driver.page_source

        content.replace('<!--', '')
        content.replace('-->', '')
        # print(content)

        content2 = etree.HTML(content)
        # 番号
        number = content2.xpath('//div[@class="works"]//h4[@class="work-id"]/text()')
        # print(number)

        description = content2.xpath('//div[@class="works"]//h4[@class="work-title"]/text()')
        # print(description)

        # 获取所有a标签的href属性
        resp = requests.get(url)
        html = etree.HTML(resp.text)
        link_list = html.xpath('//div[@class="works"]//@href')
        for i in range(len(link_list)):
            link_list[i] = 'https://javtxt.net' + link_list[i]
            # print(link_list[1])

        link_list = list(map(lambda a, b: [a, b], link_list, description))

        # print(link_list)

        video_list = dict(map(lambda a, b: [a, b], number, link_list))
        # for number, link in video_list.items():
        #     print(number, link)

        return video_list

    # 返回番号magnet
    def get_magnet(self, url):
        self.driver.get(url)

        # 获取所有a标签的href属性
        resp = requests.get(url)
        html = etree.HTML(resp.text)
        magnet_link = html.xpath('//a[@class="button btn-mag"]/@href')
        # print(magnet_link)
        self.driver.get(magnet_link[0])

        # 获取搜索页的地址，上面的是为了这步做准备
        resp = requests.get(magnet_link[0])
        html = etree.HTML(resp.text)
        magnet_link = html.xpath('//tr/td/a/@href')
        # print(magnet_link)
        for i in range(len(magnet_link)):
            magnet_link[i] = 'https://0cili.net' + magnet_link[i]
        # print(magnet_link[0])

        resp = requests.get(magnet_link[0])
        html = etree.HTML(resp.text)
        magnet_link = html.xpath('//div[@class="input-group magnet-box"]/input/@value')
        # print(magnet_link[0])

        return magnet_link[0]

    # sheet
    # 演员名字, [番号1], 描述, magnet
    #         [番号2], 描述, magnet
    #         [番号3], 描述, magnet
    #         [番号4], 描述, magnet

    def write_excel(self, url):
        for i in self.get_actresses(url).items():
            print('##########', i[0], '###########')
            # 建议在这建立名字 sheet

            # 获取番号地址
            for j in self.get_video_message(i[1]).items():
                print('_____________________')
                print('番号：', j[0])
                print('描述：', j[1][1])
                print('磁力链接：', self.get_magnet(j[1][0]))
                print('_____________________')



    def driver_quit(self, t):
        time.sleep(t)
        self.driver.quit()


if __name__ == '__main__':
    url = 'https://javtxt.net/top-actresses'
    example = MagnetSpider(url)
    # example.get_magnet()
    # example.get_video_message('https://javtxt.net/actress/18566')

    example.write_excel(example.url)


    example.driver_quit(3)

