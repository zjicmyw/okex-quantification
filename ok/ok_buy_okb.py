import okex.spot_api as spot
import json
from common import ms_sql as sql
import datetime

ms = sql.MSSQL(host="", user="", pwd="", db="")

# 记录okb的买入卖出策略


with open("database/accounts.json",'r') as load_f:
    load_dict = json.load(load_f)
    api_key=load_dict['myokapi']['api_key']
    seceret_key=load_dict['myokapi']['seceret_key']
    passphrase=load_dict['myokapi']['passphrase']

def okb():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('\033[0;34;40m\t' + nowtime + ': \033[0m')

    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)

    # get_currency 获取单一币种持仓信息
    usdt_dict = spotAPI.get_coin_account_info('USDT')


    if(float(usdt_dict['balance'])==0):
        # 获取某个ticker信息 get_specific_ticker
        okb_dict = spotAPI.get_specific_ticker('OKB-USDT')
        # best_ask 卖一价  last 最新成交价
        print(okb_dict['best_bid'])

        # todo:未完成


    # # 将这一分钟的数据存进数据库
    # print(ticker_dict)
    # string1 =str(ticker_dict).replace('\'','\'\'').replace('{','\'{').replace('}','}\'')
    # send_mail_sql1 = "insert into tab_minutes_price (token_price) values(%s)"%(string1)
    # ms.ExecNonQuery(send_mail_sql1)
    #
    #
    #
    # for item in instrument_id_list1:
    #     price_change=(float(ticker_dict[item])-float(history_list_dict[item]))/float(ticker_dict[item])
    #     if(price_change>0.005 or price_change<-0.005):
    #         print(price_change)
    #         # 将这一分钟的数据暴涨暴跌存进数据库
    #         send_mail_sql2 = "insert into tab_price_change (before_price,now_price,change) values(%s,%s,%s)" % (str(history_list_dict[item]),str(ticker_dict[item]),str(price_change))
    #         ms.ExecNonQuery(send_mail_sql2)

okb()
