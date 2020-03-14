import json
import sys
import os
# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
import okex.futures_api as future
import okex.spot_api as spot
from common import ms_sql as sql
import datetime

ms = sql.MSSQL()

with open("database/accounts.json",'r') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key=myokapi_info['api_key']
    seceret_key=myokapi_info['seceret_key']
    passphrase=myokapi_info['passphrase']


# 记录okex期货出现溢价 并发邮件
def yijia():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\033[0;34;40m\t' + nowtime + ': \033[0m')

    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)

    # get_ticker 获取全部ticker信息
    # type(bb_get_ticker): list
    bb_get_ticker = spotAPI.get_ticker()
    # type(ticker) : dict
    instrument_id_list = ['BTC-USDT', 'LTC-USDT', 'ETH-USDT', 'EOS-USDT', 'XRP-USDT', 'ETC-USDT', 'BCH-USDT',
                          'BSV-USDT']
    ticker_list = []
    for bb_ticker in bb_get_ticker:
        if bb_ticker['instrument_id'] in instrument_id_list:
            ticker_list.insert(len(ticker_list), {'name': bb_ticker['instrument_id'][0:-1],
                                                  bb_ticker['instrument_id'][0:-1]: bb_ticker['last']})
    # best_ask 卖一价  last 最新成交价

    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)

    future_get_ticker = futureAPI.get_ticker()
    mail_text = ''
    for ticket in ticker_list:
        for future_ticker in future_get_ticker:
            if ticket['name'] in future_ticker['instrument_id']:
                ticket[future_ticker['instrument_id']] = future_ticker['last']
                rate = (float(future_ticker['last']) / float(ticket[ticket['name']]) * 100 - 100)
                ticket[future_ticker['instrument_id'] + '溢价'] = '%.2f' % rate + '%'
                if (rate > 4 or rate < -5) and ('200626' in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '次季溢价:' + str('%.2f' % rate + '%')
                elif (rate > 1.6 or rate < -2) and ('200327' in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '季度溢价:' + str('%.2f' % rate + '%')
                elif (rate > 0.8 or rate < -1) and ('200327' not in future_ticker['instrument_id']) and ('200626' not in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '周溢价:' + str('%.2f' % rate + '%')
    # [{'name': 'ETH-USD', 'ETH-USD': '171.78', 'ETH-USD-190517': '170.476', 'ETH-USD-190517溢价': '-0.76%', 'ETH-USD-190628': '171.191', 'ETH-USD-190628溢价': '-0.34%', 'ETH-USD-190510': '170.634', 'ETH-USD-190510溢价': '-0.67%'}]
    # print(ticker_list)
    print(mail_text)
    sys.exit(0)
    # 判断上一次时间在2小时之前 并且时间在8点到晚上12点 则插入信息
    today = datetime.datetime.today()
    get_last_time = "select * from tab_send_email where create_time > '" + (
                datetime.datetime.now() - datetime.timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S') + "'"
    last_time = ms.ExecQueryOne(get_last_time)
    bl1=nowtime>datetime.datetime(today.year, today.month, today.day,8, 30, 0).strftime('%Y-%m-%d %H:%M:%S')
    bl2=nowtime<datetime.datetime(today.year, today.month, today.day, 23, 59, 59).strftime('%Y-%m-%d %H:%M:%S')
    bl3 =(last_time is None)
    if bl1 and bl2 and bl3 and mail_text != '':
        send_mail_sql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','okex期货出现溢价'+'" + nowtime + "','" + mail_text + "')"
        print(mail_text)
        ms.ExecNonQuery(send_mail_sql)
    else:
        # print(bl1,bl2,bl3)
        pass


yijia()
