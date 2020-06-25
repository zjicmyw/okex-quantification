from ok import future_record as bandao
from utils import ms_sql as sql, email_send as es, sms_send as sms
from apscheduler.schedulers.blocking import BlockingScheduler


ms = sql.MSSQL()
# 所有定时任务
try:
    pass
    job_defaults = {
        'coalesce': True,  # 积攒的任务只跑一次
        'max_instances': 5,  # 支持5个实例并发
        'misfire_grace_time': 600  # 600秒的任务超时容错
    }
    sched = BlockingScheduler(job_defaults=job_defaults)
    # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

    def my_email():
        es.mail()

    def my_bd():
        bandao.bd()

    sched.add_job(func=my_email, trigger='interval', seconds=90)
    sched.add_job(func=my_bd, trigger='interval', minutes=4)
    sched.start()
except Exception as e:
    sms.send_wrong_sms()
    newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','定时任务出现问题'+'" + \
        nowtime + "','" + str(e) + "')"
    print(str(e))
    ms.ExecNonQuery(newsql)
