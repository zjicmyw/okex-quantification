# coding=utf-8
import datetime
from utils import ms_sql as sql
from utils import sms_send
import logging

# 邮件
ms = sql.MSSQL()
address_to = 'e7lian@qq.com'

# 日志
logging.basicConfig(level=logging.WARNING,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='log1.txt',
                    filemode='w')
logger = logging.getLogger(__name__)

def warning(data):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now_time + '--' + data)
    logger.warning(now_time + '--' + data)


'''
时间打印
'''


def time_print(title):
    now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(title + now_time)


'''
报警邮件
类型1：检测到和上次不同时，发送提醒邮件
'''


def alert_mail_1(mail_subject, mail_text, mail_type, sms_text):
    sql_send_mail = ''
    try:
        sql_get_last = "select top 1 mail_text from tab_send_email where type=%d order by create_time desc" % (
            mail_type)
        last_text = ms.ExecQueryOne(sql_get_last)
        if last_text is not None:
            if mail_text != last_text[0]:
                sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('%s','%s','%s',%d)" % (
                    address_to, mail_subject, mail_text, mail_type)
            else:
                print('相同,不发送邮件')
        else:
            sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('%s','%s','%s',%d)" % (
                address_to, mail_subject, mail_text, mail_type)
        if sql_send_mail != '':
            print('发送邮件', mail_subject, mail_text)
            sms_result = sms_send.send(sms_text, False)
            print(sms_result)
            ms.ExecNonQuery(sql_send_mail)
            return True
        else:
            return False

    except Exception as e:
        print('tools.py/tools-alert_mail_1 出現异常:', e)
        print(sql_get_last)
        print(sql_send_mail)
        return False


'''
报警邮件
判断上一次发送时间在2小时之前 并且时间在8点到晚上12点 ，发送提醒邮件
'''


def alert_mail_2(mail_subject, mail_text, mail_type):
    sql_send_mail = ''
    now_time = datetime.datetime.now()
    # 2小时之前的时间
    time_2_before = (now_time - datetime.timedelta(hours=2)
                     ).strftime('%Y-%m-%d %H:%M:%S')
    try:
        sql_alert_count = "select count(*) from tab_send_email where type=%d and create_time > '%s'" % (
            mail_type, time_2_before)
        # 2小时内发送提醒的次数
        alert_count = ms.ExecQueryOne(sql_alert_count)

        bl1 = now_time > datetime.datetime(
            now_time.year, now_time.month, now_time.day, 8, 30, 0)
        bl2 = now_time < datetime.datetime(
            now_time.year, now_time.month, now_time.day, 23, 59, 59)
        bl3 = (alert_count == 0)
        print(bl1, bl2, bl3)
        if bl1 and bl2 and bl3:
            sql_send_mail = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('%s','%s','%s',%d)" % (
                address_to, mail_subject, mail_text, mail_type)
            ms.ExecNonQuery(sql_send_mail)
        else:
            pass
    except Exception as e:
        print('tools.py/tools-alert_mail_2 出現异常:', e)
        print(sql_alert_count)
        print(sql_send_mail)


def get_buy_account_list():
    return ms.ExecQueryALL(
        "select keyvalue,api_key,seceret_key,passphrase,order_instrument_id,order_size from tab_accounts where status =2")


def get_account_bykeyvalue(keyvalue):
    return ms.ExecQueryOne(
        "select api_key,seceret_key,passphrase,order_instrument_id,order_size from tab_accounts where status =2 and keyvalue='{}'".format(keyvalue))
