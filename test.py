import requests
import time
import random
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



# 下载视频详情页面中的视频
def loadVideo(url):
    # url: https://www.pearvideo.com/video_1766100
    videoStatusUrl = 'https://www.pearvideo.com/videoStatus.jsp'
    # ?contId=1766100&mrd=0.09795100838242665
    contId = url.split('_')[1]
    params = {
        'contId': contId,
        'mrd': random.random()
    }
    key = parse.urlencode(params)
    #print(key)
    videoStatusUrl = videoStatusUrl + '?' + key
    #print(videoStatusUrl)
    time.sleep(1) # 延时1秒再爬取
    userAgent = random.choice(ua_list)
    headers = {
        'User-Agent': userAgent,
        'Referer': url, # 模拟从url中发送请求
    }
    # 发送请求
    proxies = {
        'http': 'http://127.0.0.1:8888',
        'https': 'http://127.0.0.1:8888',
    }
    response = requests.get(url=videoStatusUrl, headers=headers, proxies=proxies, verify=False)
    # 获取响应的内容
    content = response.json()
    srcUrl = content['videoInfo']['videos']['srcUrl']
    #print(srcUrl)
    # 下载地址被伪装了
    # 运行的结果如下，不能正常打开
    # https://video.pearvideo.com/mp4/third/20220623/1656142448942-13293812-222901-hd.mp4
    # 正确的地址应该是：
    # https://video.pearvideo.com/mp4/third/20220623/cont-1766100-13293812-222901-hd.mp4
    # 关键是把13位数字替换成 cont-{contId} 才行
    import re
    srcUrl = re.sub('/\d{13}-','/cont-%s-' % contId, srcUrl)
    print(srcUrl)
    return srcUrl


if __name__ == '__main__':
    url = 'https://www.pearvideo.com/category_5'
    loadVideo('https://www.pearvideo.com/video_1766028')
