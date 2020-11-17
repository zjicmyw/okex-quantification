import requests
from pyquery import PyQuery as pq
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import socket
import socks
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 10808)
socket.socket = socks.socksocket


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}

last_title = ''


class MySpider(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_onePage(self):
        get_url = self.base_url
        response = requests.get(url=get_url, headers=headers)
        if response.status_code == 200:
            return response.content.decode()
        else:
            return None

    def parse_onePage(self, html):
        pq_html = pq(html)
        ul = pq_html('.article-list .article-list-item:first a').text()
        global last_title
        if last_title != ul:
            last_title = ul
            if "提币" in ul and ul != 'OKEx关于暂停提币功能后相关事件进展的公告':
                print('新增提币相关')
                send()
            else:
                print('新增公告：'+ul)
        else:
            print('无新增公告：'+ul)


sms = {
    "sms_url": "http://61.191.26.189:8888/smser.ashx",
    "sms_data": {
        "f": "2",
        "uid": "70944",
        "un": "dkgzs",
        "pw": "ecff204e937d945e",
        "p": "13777842815",
        "i": ""
    },
    "phone": "13777842815"
}


def send():
    sms_data = sms['sms_data']
    sms_data['i'] = "请查看异常天气"
    res = requests.get(url=sms['sms_url'], params=sms_data)
    return(res.text)


# 所有定时任务
try:

    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 10,  # 支持10个实例并发
        'misfire_grace_time': 600  # 600秒的任务超时容错
    }
    sched = BlockingScheduler(job_defaults=job_defaults)
    # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

    def test():

        base_url = 'https://www.okex.com/support/hc/zh-cn/sections/360009208032-%E5%85%85%E6%8F%90%E6%9A%82%E5%81%9C-%E6%81%A2%E5%A4%8D%E5%85%AC%E5%91%8A'
        my_spider = MySpider(base_url)
        result_html = my_spider.get_onePage()
        my_spider.parse_onePage(result_html)

    # test()
    sched.add_job(func=test, trigger='interval', seconds=120)
    sched.start()
except Exception as e:
    send()
