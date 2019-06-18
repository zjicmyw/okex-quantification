import io
import sys
import random
import time
import requests
from bs4 import BeautifulSoup

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

def open_url(url_str,proxy_ip):
    html = ""
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
        "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding":"gzip, deflate",
        "Connection":"keep-alive"
    }
    if bool(proxy_ip):
        html = requests.get(url=url_str,headers = headers, proxies=proxy_ip).content
    else:
        html = requests.get(url=url_str,headers = headers).content
    #返回网页内容,动态加载的需要另行处理
    return html



'''
该脚本使用说明:

使用免费的代理或者自己购买的代理,打开指定的网页地址,模拟用户使用独立IP访问相同页面
这里演示,使用的是89免费代理,地址:http://www.89ip.cn/
可以使用http://filefab.com/查看IP

http_ip:
可以自行编辑添加更多代理
url_str:
可以自行编辑为需要打开的网页地址

'''

url_str = 'https://www.feixiaohao.com/search/?word='

print("访问的网页地址:",url_str)

http_ip = [
    '119.101.117.134:9999',
    '125.40.238.181:56738',
    '139.198.191.107:1080',
    '106.15.42.179:33543',
    '183.185.78.49:80'
]

'''
循环执行,每次访问后等待指定时间后重新访问,避免过于频繁
max_count:
可以自行编辑,访问多少次后自动终止
sleep_time:
可以自行编辑,等待多久后重新发起新的独立IP访问
'''

flag = True
max_count = 3
sleep_time = 3

print('共计需要访问',url_str,'网页',max_count,'次')

# 这里只做简单演示请求,单次延时访问,并发可以使用asyncio,aiohttp
while flag:
    proxy_ip = {
        'http' : random.choice(http_ip),
    }

    print('使用代理的IP:',proxy_ip)
    html = open_url(url_str,proxy_ip)

    # 解析网页内容,可以使用BeautifulSoup
    print('返回网页内容长度:',len(html))

    time.sleep(sleep_time)
    print('等待',sleep_time,'秒后,重新使用独立IP发起网页请求')

    max_count -=1

    if(max_count==0):
        flag = False

print("执行结束")