import requests
import json
import time
import datetime
from dateutil.parser import parse
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
}


class MyJsonSpider(object):
    def __init__(self, base_url):
        self.base_url = base_url

    def get_onePage(self):
        get_url = self.base_url
        response = requests.get(url=get_url, headers=headers)
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return None

    def parse_onePage_json(self, result_json):
        post_list = []
        job_list = []

        dict_result = json.loads(result_json)
        if dict_result['code'] == 10000:
            post_list = dict_result['data']['result']
            timestamp = post_list[0]['timestamp']
            timestruct = time.localtime(timestamp)
            # 2016-12-22 10:49:57
            t1 = time.strftime('%Y-%m-%d %H:%M:%S', timestruct)
            print(t1)
            get_interview(t1)

        else:
            print('访问错误')

        return job_list


def get_interview(t1):
    now = datetime.datetime.now()
    t2 = now.strftime('%Y-%m-%d %H:%M:%S')
    date1 = parse(t1)
    date2 = parse(t2)
    result = (date2 - date1).total_seconds()
    print(result)
    if result < 300:
        send()



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

        base_url = 'https://api.yitaifang.com/index/tokenTransaction/?page=1&a=0x3800544c0ad45e2222d67151ff08ee0c476f6221'
        my_spider = MyJsonSpider(base_url)

        result_json = my_spider.get_onePage()

        job_list = my_spider.parse_onePage_json(result_json)

    sched.add_job(func=test, trigger='interval', seconds=120)

    sched.start()
except Exception as e:
    send()
