import schedule
import ok_price_history as okph
import time
import email_send as es
import ms_sql as sql
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

ms = sql.MSSQL(host="", user="", pwd="", db="")
# 所有定时任务
try:
   sched = BlockingScheduler()
   # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

   def my_email():
      es.mail()
   def my_yijia():
      okph.yijia()

   sched.add_job(func=my_email, trigger='interval', minutes=1)
   sched.add_job(func=my_yijia, trigger='interval', minutes=3)
   sched.start()
except Exception as e:
   newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','okex脚本出现问题'+'" + nowtime + "','" + str(e) + "')"
   print(str(e))
   ms.ExecNonQuery(newsql)