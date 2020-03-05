# coding=utf-8
import json
import datetime
import sys
import os
# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from common import ms_sql as sql
import okex.spot_api as spot

ms = sql.MSSQL(host="", user="", pwd="", db="")

with open("database/accounts.json", 'r') as load_f:
    load_dict = json.load(load_f)
    api_key = load_dict['myokapi']['api_key']
    seceret_key = load_dict['myokapi']['seceret_key']
    passphrase = load_dict['myokapi']['passphrase']


# 记录okexBTC现货量化下单 并发邮件
def bd():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('现货量化检测：'+'\033[0;34;40m\t' + nowtime + ': \033[0m')

    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
    result = spotAPI.get_orders_list(state='2',instrument_id='BTC-USDT')


    # side	String	buy 或 sell
    # price_avg	String	成交均价
    # created_at 时间


    mail_text='' # 邮件内容
    my_last_spot1=result[0][0] # 我的最新一次下单数据
    my_last_spot2=result[0][1] # 我的最新二次下单数据

    mail_text='最新一次时间:{0},动作：{1}，成交均价{2};'.format(my_last_spot1['created_at'],my_last_spot1['side'],my_last_spot1['price_avg'])
    mail_text+='上两次时间:{0},动作：{1}，成交均价{2};'.format(my_last_spot2['created_at'],my_last_spot2['side'],my_last_spot2['price_avg'])
   

    get_last_text = "select top 1 mail_text from tab_send_email where type=1 order by create_time desc"
    last_text = ms.ExecQueryOne(get_last_text)

    # 如果邮件内容不为空，并且和上次不同，插入数据库，以发送提醒邮件
    if mail_text != '' and mail_text != last_text[0]:
        send_mail_sql = "insert into tab_send_email (address_to,mail_subject,mail_text,type) values('e7lian@qq.com','现货开单','" + mail_text + "','1')"
        print(mail_text)
        ms.ExecNonQuery(send_mail_sql)
    else:
        print('相同')

