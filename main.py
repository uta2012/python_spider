import tieba6
import time


time.
if __name__ == '__main__':
    kw = input('请输入要爬取的贴吧：')
    beginPage = int(input('请输入开始页：'))
    endPage = int(input('请输入结束页：'))
    key = tieba6.parse.urlencode({'kw': kw})  # kw=%E6%B5%B7%E8%B4%BC%E7%8E%8B
    url = 'https://tieba.baidu.com/f?' + key
    print(url)
    tieba6.tiebaSpider(url, beginPage, endPage)
