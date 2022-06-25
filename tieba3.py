import requests
import random
import time

from urllib import parse

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER'
]

# 加载一个页面
def loadPage(url):
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

    return content


def writePage(html, filename):
    print('正在保存到：', filename)
    f = open(filename, 'w', encoding='utf-8')
    f.write(html)
    f.close()



def tiebaSpider(url, beginPage, endPage):
    for page in range(beginPage, endPage+1):
        pn = 50*(page-1)
        fullurl = url + '&pn=' + str(pn)
        content = loadPage(fullurl)
        filename = '第%d页.html' % page
        writePage(content, filename)


# 加载一个页面
# url = 'https://tieba.baidu.com/f?kw=%E6%98%BE%E5%8D%A1'
# print(loadPage(url))
# writePage(loadPage(url), '显卡吧.html')

# tiebaSpider(url, 1, 4)


if __name__ == '__main__':
    kw = input('请输入要爬取的贴吧：')
    beginPage = int(input('请输入起始页：'))
    endPage = int(input('请输入终止页：'))
    key = parse.urlencode({'kw': kw})  # kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B
    url = 'https://tieba.baidu.com/f?' + key
    print(url)
    tiebaSpider(url, beginPage, endPage)





