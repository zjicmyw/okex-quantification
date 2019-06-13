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
from string import Template

ms = sql.MSSQL(host="", user="", pwd="", db="")

# 记录okex暴涨暴跌

with open("database/accounts.json",'r') as load_f:
    load_dict = json.load(load_f)
    api_key=load_dict['myokapi']['api_key']
    seceret_key=load_dict['myokapi']['seceret_key']
    passphrase=load_dict['myokapi']['passphrase']

def skyrocketing():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\033[0;34;40m\t' + nowtime + ': \033[0m')

    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)

    # get_ticker 获取全部ticker信息
    # type(bb_get_ticker): list
    bb_get_ticker = spotAPI.get_ticker()
    # type(ticker) : dict
    instrument_id_list1 = ['BTC-USDT', 'LTC-USDT', 'ETH-USDT', 'EOS-USDT', 'XRP-USDT', 'ETC-USDT', 'BCH-USDT']
    instrument_id_list2 = ('BTC-USDT', 'LTC-USDT', 'ETH-USDT', 'EOS-USDT', 'XRP-USDT', 'ETC-USDT', 'BCH-USDT')
    ticker_dict = dict.fromkeys(instrument_id_list2)
    for bb_ticker in bb_get_ticker:
        if bb_ticker['instrument_id'] in ticker_dict:
            ticker_dict[bb_ticker['instrument_id']]=bb_ticker['last']

    # best_ask 卖一价  last 最新成交价


    # 将前一分钟的数据取出数据库
    history_list_sql = "select top 1 token_price from tab_minutes_price order by create_time desc"
    history_list_ms = ms.ExecQueryOne(history_list_sql)
    history_list_dict = eval(history_list_ms[0])
    print(history_list_dict)


    # 将这一分钟的数据存进数据库
    print(ticker_dict)
    string1 =str(ticker_dict).replace('\'','\'\'').replace('{','\'{').replace('}','}\'')
    send_mail_sql1 = "insert into tab_minutes_price (token_price) values(%s)"%(string1)
    ms.ExecNonQuery(send_mail_sql1)



    for item in instrument_id_list1:
        price_change=(float(ticker_dict[item])-float(history_list_dict[item]))/float(ticker_dict[item])
        if(price_change>0.005 or price_change<-0.005):
            print(price_change)
            # 将这一分钟的数据暴涨暴跌存进数据库
            send_mail_sql2 = "insert into tab_price_change (before_price,now_price,change) values(%s,%s,%s)" % (str(history_list_dict[item]),str(ticker_dict[item]),str(price_change))
            ms.ExecNonQuery(send_mail_sql2)

skyrocketing()
