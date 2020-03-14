# coding=utf-8
from common import ms_sql as sql
ms = sql.MSSQL()

# 报警邮件
def alert_mail(mail_subject, mail_text, mail_type):
    sql_send_mail=''
    try:
        sql_get_last = "select top 1 mail_text from tab_send_email where type=%d order by create_time desc" % (
            mail_type)
        last_text = ms.ExecQueryOne(sql_get_last)
        if last_text is not None:
            # 如果邮件内容不为空，并且和上次不同，插入数据库，以发送提醒邮件
            if mail_text != last_text[0]:
                sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','%s','%s',%d)" % (mail_subject, mail_text, mail_type)              
            else:
                print('相同,不发送邮件')
        else:
                sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','%s','%s',%d)" % (mail_subject, mail_text, mail_type)
        if sql_send_mail !='':
            print('发送邮件',mail_subject, mail_text)
            ms.ExecNonQuery(sql_send_mail)

    except Exception as e:
        print('Common/tools-alert_mail 出現异常:',e)
        print(sql_get_last)
        print(sql_send_mail)

