from ok import check_future_account_v5 as record
from utils import ms_sql as sql, email_send as es, sms_send as sms, tools
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
import logging
import time

ms = sql.MSSQL()
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.WARNING)


# 所有定时任务
try:

    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 10,  # 支持10个实例并发
        'misfire_grace_time': 600  # 600秒的任务超时容错
    }
    sched = BlockingScheduler(job_defaults=job_defaults)
    # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

    # 检测下单
    def my_record():
        record.okex_v5()

    def my_listener(event):
        if event.exception:
            print('任务出错了。')
            # sms.send_wrong_sms()
            sched.shutdown()
            time.sleep(5)
            sched.start()
        else:
            pass

    my_record()
    
    sched.add_job(func=my_record, trigger='interval', hours=1)
   
    sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    sched._logger = logging
    sched.start()
except Exception as e:
    # sms.send_wrong_sms()
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','定时任务出现问题'+'" + \
        nowtime + "','" + str(e) + "')"
    tools.warning(str(e))
    ms.ExecNonQuery(newsql)
    sched.shutdown()
    time.sleep(5)
    sched.start()
