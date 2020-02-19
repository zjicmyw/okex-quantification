import json
import datetime
import sys
from common import ms_sql as sql
import okex.futures_api as future

ms = sql.MSSQL(host="", user="", pwd="", db="")

with open("database/accounts.json",'r') as load_f:
    load_dict = json.load(load_f)
    api_key=load_dict['myokapi']['api_key']
    seceret_key=load_dict['myokapi']['seceret_key']
    passphrase=load_dict['myokapi']['passphrase']


# 记录okex期货量化下单 并发邮件
def bd():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('量化检测：'+'\033[0;34;40m\t' + nowtime + ': \033[0m')

    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
    result = futureAPI.get_specific_position('BTC-USD-200327') 
    # long_qty  short_qty 空仓数量
    # long_avg_cost  short_avg_cost 开仓平均价 
    # long_settlement_price short_settlement_price  结算基准价
    

    mail_text='' # 邮件内容
    my_future=result['holding']# 我的量化数据
    if my_future[0]['long_qty']=='0':
        mail_text=my_future[0]['short_avg_cost']+'开空。上次动作：'+my_future[0]['long_avg_cost']+'开多，'+my_future[0]['long_settlement_price']+'平多'
    else:
        mail_text=my_future[0]['long_avg_cost']+'开多。上次动作：'+my_future[0]['long_avg_cost']+'开空，'+my_future[0]['long_settlement_price']+'平空'

    
    get_last_text = "select top 1 mail_text from tab_send_email order by create_time desc"
    last_text = ms.ExecQueryOne(get_last_text)

    # 如果邮件内容不为空，并且和上次不同，插入数据库，以发送提醒邮件
    if mail_text != '' and mail_text != last_text[0]: 
        send_mail_sql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','半岛检测','" + mail_text + "')"
        print(mail_text)
        ms.ExecNonQuery(send_mail_sql)
    else:
        print('相同')
