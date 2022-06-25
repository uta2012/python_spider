import requests
import time
import random
from lxml import etree
from urllib import parse
import re
import os

import urllib.request

ua_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44',
    "Mozilla/4.0(compatible;MSIE6.0;WindowsNT5.1;SV1;AcooBrowser;.NETCLR1.1.4322;.NETCLR2.0.50727)",
    "Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0;AcooBrowser;SLCC1;.NETCLR2.0.50727;MediaCenterPC5.0;.NETCLR3.0.04506)",
    "Mozilla/4.0(compatible;MSIE7.0;AOL9.5;AOLBuild4337.35;WindowsNT5.1;.NETCLR1.1.4322;.NETCLR2.0.50727)",
    "Mozilla/5.0(Windows;U;MSIE9.0;WindowsNT9.0;en-US)",
    "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Win64;x64;Trident/5.0;.NETCLR3.5.30729;.NETCLR3.0.30729;.NETCLR2.0.50727;MediaCenterPC6.0)",
    "Mozilla/5.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0;WOW64;Trident/4.0;SLCC2;.NETCLR2.0.50727;.NETCLR3.5.30729;.NETCLR3.0.30729;.NETCLR1.0.3705;.NETCLR1.1.4322)",

]


# 加载一个页面
def loadPage(url):
    print('------loadPage------')
    # User-Agent伪装
    userAgent = random.choice(ua_list)
    headers = {
        'User-Agent': userAgent
    }
    # 发送请求
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888'
    }
    response = requests.get(url, headers=headers, proxies=proxies, verify=False)

    # 获取响应的内容
    content = response.text

    # 去掉恶意注释<！-- -->
    content = content.replace('<!--', '')
    content = content.replace('-->', '')

    # print(content)
    content2 = etree.HTML(content)
    link_list = content2.xpath('//li[@class="categoryem"]/div[@class="vervideo-bd"]/a')
    #print(content2)
    for link in link_list:

        full_link = 'https://www.pearvideo.com/' + link.xpath('./@href')[0]
        full_name = link.xpath('./div[@class="vervideo-title"]/text()')[0]
        long = link.xpath('.//div[@class="cm-duration"]/text()')[0]
        print('视频地址：%s 视频标题：%s 时长：%s' % (full_link, full_name, long))
        loadvideo(full_link)
        savevideo(loadvideo(full_link), full_link.split('/')[-1])
    # return content


# 下载详情页的视频
def loadvideo(url):
    # url: https://www.pearvideo.com/video_1766028
    # https://www.pearvideo.com/videoStatus.jsp?contld=1766028&mrd=0.627577628198944
    video_status_url = 'https://www.pearvideo.com/videoStatus.jsp'
    contId = url.split('_')[1]
    # print(contId)
    params = {
        'contId': contId,   # 1766028
        'mrd': random.random()  # 0.627577628198944
    }
    key = parse.urlencode(params)   # 字典转成url格式
    # print(key)
    video_status_url = video_status_url + '?' + key
    # print(video_status_url)

    time.sleep(1)

    userAgent = random.choice(ua_list)
    headers = {
        'Referer': url,
        'User-Agent': userAgent,
    }

    # 发送请求
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888'
    }

    response = requests.get(url=video_status_url, headers=headers, proxies=proxies, verify=False)

    # 获取响应内容
    content = response.json()
    # print(content)

    srcUrl = content['videoInfo']['videos']['srcUrl']
    # print(srcUrl)

    srcUrl = re.sub('/\d{13}-', '/cont-%s-' % contId, srcUrl)
    # https://video.pearvideo.com/mp4/third/20220623/cont-1766092-10787886-194050-hd.mp4
    # print(srcUrl)
    return srcUrl

def savevideo(url, name):
    if not os.path.exists('video'):
        os.mkdir('video')
    print('开始下载《%s》...........'%name)
    urllib.request.urlretrieve(url, r"./video/%s.mp4" % name)
    print('《%s》下载完毕！' % name)



if __name__ == '__main__':
    url = 'https://www.pearvideo.com/category_5'
    loadPage(url)
    #loadvideo('https://www.pearvideo.com/video_1766028')




