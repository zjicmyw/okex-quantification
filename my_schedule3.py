from ok import ok_bandao as bandao
from common import ms_sql as sql, email_send as es
from apscheduler.schedulers.blocking import BlockingScheduler
# import logging

# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

ms = sql.MSSQL(host="", user="", pwd="", db="")
# 所有定时任务
try:
   sched = BlockingScheduler()
   # 有date, interval, cron可供选择，其实看字面意思也可以知道，date表示具体的一次性任务，interval表示循环任务，cron表示定时任务

   def my_email():
      es.mail()
   def my_bd():
      bandao.bd()

   sched.add_job(func=my_email, trigger='interval', seconds=90)
   sched.add_job(func=my_bd, trigger='interval', minutes=4)
   sched.start()
except Exception as e:
   newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','定时任务出现问题'+'" + nowtime + "','" + str(e) + "')"
   print(str(e))
   ms.ExecNonQuery(newsql)