import json
import time
import sys
import os
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from utils import tools
from okex_sdk_api.okex import futures_api as future

with open(o_path+"/json/accounts.json", 'r') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key = myokapi_info['api_key']
    seceret_key = myokapi_info['seceret_key']
    passphrase = myokapi_info['passphrase']
futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)

instrument = 'BTC-USD-200626'
# 记录okex期货下单 并发邮件

def bd():
    tools.time_print('期货检测')
    mail_text = ''  # 邮件内容
    long_order=True
    try:
        result = futureAPI.get_specific_position(instrument)
        # long_qty  short_qty 空仓数量
        # long_avg_cost  short_avg_cost 开仓平均价
        # long_settlement_price short_settlement_price  结算基准价
        my_future = result['holding'][0]  # 我的量化数据
        if my_future['long_qty'] == '0':
            mail_text = '{}平多套保。上次动作：{}开多'.format(my_future['short_avg_cost'],my_future['long_avg_cost'])
            long_order=False    
        else:
            mail_text = '{}平空开多。上次动作：{}开空'.format(my_future['long_avg_cost'],my_future['short_avg_cost'])
            long_order=True 
    except Exception as e:
        print("future_record.py -bd()出現异常:", e)

    if mail_text != '':
        mail_result = tools.alert_mail_1('期货开单', mail_text, 2)
        # 如果期货开单，则其他账户执行买入
        if mail_result:
            take_order(long_order)


'''
type
1:开多2:开空3:平多4:平空
order_type
4：市价委托
'''
def take_order(long_order):
    try:
        account_list = tools.get_buy_account_list()
        for account in account_list:
            keyvalue,buy_api_key,buy_seceret_key,buy_passphrase,buy_instrument,order_size = account#拆包
            buy_futureAPI = future.FutureAPI(buy_api_key, buy_seceret_key, buy_passphrase, True)
            if long_order:
                print('平空')
                buy_result1 = buy_futureAPI.take_order(buy_instrument, '4','',size=order_size, order_type='4')
                print('开多')
                time.sleep(2)
                buy_result2 = buy_futureAPI.take_order(buy_instrument, '1','',size=order_size, order_type='4')
            else:
                print('平多')
                buy_result1 = buy_futureAPI.take_order(buy_instrument, '3','',size=order_size, order_type='4')
                print('开空')
                time.sleep(2)
                buy_result2 = buy_futureAPI.take_order(buy_instrument, '2','',size=order_size, order_type='4')
            print(keyvalue,buy_result1,buy_result2,sep='\n')
            time.sleep(5)
    except Exception as e:
        print("future_record.py -take_order()出現异常:", e)


if __name__ == "__main__":
    bd()
