from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from common import ms_sql as sql

# 将 数据表 tab_send_email 未发送的邮件 发送 并标记为已发送


ms = sql.MSSQL(host="", user="", pwd="", db="")

with open("database/accounts.json", 'r') as load_f:
    load_dict = json.load(load_f)
    mail_info = load_dict['mail_info']

def send():
    # 这里使用SMTP_SSL就是默认使用465端口
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(1)

    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(mail_info["mail_text"], "plain", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]

    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())

    smtp.quit()


def mail():
    sendlist = ms.ExecQueryALL(
        "select address_to,mail_subject,mail_text from tab_send_email where status =1")

    for item in sendlist:
        mail_info["to"] = list(item)[0]
        mail_info["mail_subject"] = list(item)[1]
        mail_info["mail_text"] = list(item)[2]
        send()

        newsql = "update tab_send_email set status =0 where mail_text='" + mail_info[
            "mail_text"] + "' and mail_subject='" + mail_info["mail_subject"] + "' and address_to='" + mail_info[
                     "to"] + "' and status = 1 "
        ms.ExecNonQuery(newsql)
