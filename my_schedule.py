from ok import future_record as bandao
from utils import ms_sql as sql, email_send as es, sms_send as sms
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging

ms = sql.MSSQL()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='a')


# 所有定时任务
try:
    pass
    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 10,  # 支持10个实例并发
        'misfire_grace_time': 600  # 600秒的任务超时容错
    }
    sched = BlockingScheduler(job_defaults=job_defaults)
    # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

    def my_email():
        es.mail()

    def my_bd():
        bandao.bd()

    def my_listener(event):
        if event.exception:
            print('任务出错了。')
        else:
            pass

    sched.add_job(func=my_email, trigger='interval', seconds=60)
    sched.add_job(func=my_bd, trigger='interval', minutes=2)
    sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    sched._logger = logging
    sched.start()
except Exception as e:
    sms.send_wrong_sms()
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','定时任务出现问题'+'" + \
        nowtime + "','" + str(e) + "')"
    print(str(e))
    ms.ExecNonQuery(newsql)
