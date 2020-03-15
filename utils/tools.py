# coding=utf-8
import datetime
from common import ms_sql as sql
ms = sql.MSSQL()


'''
时间打印
'''


def time_print(title):
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(title+'\033[0;34;40m\t' + nowtime + ': \033[0m')


'''
报警邮件
类型1：检测到和上次不同时，发送提醒邮件
'''


def alert_mail_1(mail_subject, mail_text, mail_type):
    sql_send_mail = ''
    try:
        sql_get_last = "select top 1 mail_text from tab_send_email where type=%d order by create_time desc" % (
            mail_type)
        last_text = ms.ExecQueryOne(sql_get_last)
        if last_text is not None:
            if mail_text != last_text[0]:
                sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','%s','%s',%d)" % (
                    mail_subject, mail_text, mail_type)
            else:
                print('相同,不发送邮件')
        else:
            sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','%s','%s',%d)" % (
                mail_subject, mail_text, mail_type)
        if sql_send_mail != '':
            print('发送邮件', mail_subject, mail_text)
            ms.ExecNonQuery(sql_send_mail)

    except Exception as e:
        print('Common/tools-alert_mail_1 出現异常:', e)
        print(sql_get_last)
        print(sql_send_mail)


'''
报警邮件
判断上一次发送时间在2小时之前 并且时间在8点到晚上12点 ，发送提醒邮件
'''


def alert_mail_2(mail_subject, mail_text, mail_type):
    sql_send_mail = ''
    today = datetime.datetime.today()
    # 2小时之前的时间
    time_2_before=(datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
    try:
        sql_get_last_time = "select * from tab_send_email where type=%d and create_time > '%s'" % (
            mail_type,time_2_before)
        # 上一次发送的时间
        last_time = ms.ExecQueryOne(sql_get_last_time)

        bl1 = nowtime > datetime.datetime(
            today.year, today.month, today.day, 8, 30, 0).strftime('%Y-%m-%d %H:%M:%S')
        bl2 = nowtime < datetime.datetime(
            today.year, today.month, today.day, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
        bl3 = (last_time is None)
        print(bl1,bl2,bl3)
        if bl1 and bl2 and bl3 :
            sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','%s','%s',%d)" % (
                    mail_subject, mail_text, mail_type)
            ms.ExecNonQuery(send_mail_sql)
        else:
            print(bl1,bl2,bl3)
            print('进入了else')
    except Exception as e:
        print('Common/tools-alert_mail_2 出現异常:', e)
        print(sql_get_last)
        print(sql_send_mail)
    