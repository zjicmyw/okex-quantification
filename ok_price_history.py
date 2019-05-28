import okex.account_api as account
import okex.ett_api as ett
import okex.futures_api as future
import okex.lever_api as lever
import okex.spot_api as spot
import okex.swap_api as swap
import json
import ms_sql as sql
import schedule
import time
import sys
import datetime

ms = sql.MSSQL(host="", user="", pwd="", db="")

with open("database/accounts.json",'r') as load_f:
    load_dict = json.load(load_f)
    api_key=load_dict['myokapi']['api_key']
    seceret_key=load_dict['myokapi']['seceret_key']
    passphrase=load_dict['myokapi']['passphrase']


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
                if (rate > 3 or rate < -3) and ('190628' in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '季度溢价:' + str('%.2f' % rate + '%')
                elif (rate > 1 or rate < -1) and ('190628' not in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '周溢价:' + str('%.2f' % rate + '%')
    # [{'name': 'ETH-USD', 'ETH-USD': '171.78', 'ETH-USD-190517': '170.476', 'ETH-USD-190517溢价': '-0.76%', 'ETH-USD-190628': '171.191', 'ETH-USD-190628溢价': '-0.34%', 'ETH-USD-190510': '170.634', 'ETH-USD-190510溢价': '-0.67%'}]
    # print(ticker_list)
    # print(mail_text)
    # sys.exit(0)
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


# yijia()
