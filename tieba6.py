import requests
import random
import time
import os
from lxml import etree

from urllib import parse

ua_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1;SV1;AcooBrowser;.NETCLR1.1.4322;.NETCLR2.0.50727)",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0;AcooBrowser;SLCC1;.NETCLR2.0.50727;MediaCenterPC5.0;.NETCLR3.0.04506)",
    "Mozilla/4.0(compatible;MSIE7.0;AOL9.5;AOLBuild4337.35;WindowsNT5.1;.NETCLR1.1.4322;.NETCLR2.0.50727)",
    "Mozilla/5.0(Windows;U;MSIE9.0;WindowsNT9.0;en-US)",
    "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Win64;x64;Trident/5.0;.NETCLR3.5.30729;.NETCLR3.0.30729;.NETCLR2.0.50727;MediaCenterPC6.0)",
    "Mozilla/5.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0;WOW64;Trident/4.0;SLCC2;.NETCLR2.0.50727;.NETCLR3.5.30729;.NETCLR3.0.30729;.NETCLR1.0.3705;.NETCLR1.1.4322)",

]


def writeImage(url):
    print('------writeImage------')
    time.sleep(1)
    userAgents = random.choice(ua_list)
    headers = {
        'User-Agent': userAgents
    }
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888'
    }
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    content = response.content# 获取二进制数据
    print('url：' + url)
    filename = url[-10:]
    print('filename：' + filename)
    if not os.path.exists('img'):
        os.mkdir('img')
    f = open('img/' + filename, 'wb')
    f.write(content)
    f.close()


def loadImage(url):
    print('------loadImage------')
    time.sleep(1)
    userAgents = random.choice(ua_list)
    headers = {
        'User-Agent': userAgents
    }
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888'
    }
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    content = response.text
    content = content.replace('<!--', '')
    content = content.replace('-->', '')

    content2 = etree.HTML(content)
    link_list = content2.xpath('//img[@class="BDE_Image"]/@src')
    for link in link_list:
        link = link.split('?')[0]
        print(link)
        writeImage(link)


# 加载一个页面
def loadPage(url):
    print('------loadPage------')
    # User-Agent伪装
    time.sleep(1)
    userAgent = random.choice(ua_list)
    headers = {
        'User-Agent': userAgent
    }
    # 发送请求
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888',
    }
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)
    # 获取响应的内容
    content = response.text
    # 去掉恶意注释<！-- -->
    content = content.replace('<!--', '')
    content = content.replace('-->', '')

    # print(content)
    content2 = etree.HTML(content)
    link_list = content2.xpath('//a[contains(@class,"j_th_tit")]/@href')
    # print(content2)
    for link in link_list:
        # print(link)
        fullink = 'https://tieba.baidu.com' + link# /p/321321312
        print(fullink)
        loadImage(fullink)
    # return content


def writePage(html, filename):
    print('正在保存到：', filename)
    f = open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()


def tiebaSpider(url, beginPage, endPage):
    for page in range(beginPage, endPage+1):
        pn = 50*(page-1)
        fullurl = url + '&pn=' + str(pn)
        # content = loadPage(fullurl)
        filename = '第%d页.html' % page
        # writePage(content, filename)
        loadPage(fullurl)
    return 'succeed!'


if __name__ == '__main__':
    kw = input('请输入要爬取的贴吧：')
    beginPage = int(input('请输入开始页：'))
    endPage = int(input('请输入结束页：'))
    key = parse.urlencode({'kw': kw})  # kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B
    url = 'https://tieba.baidu.com/f?' + key
    print(url)
    tiebaSpider(url, beginPage, endPage)



