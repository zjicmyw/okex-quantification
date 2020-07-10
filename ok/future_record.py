import json
import time
import sys
import os
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from utils import tools,sms_send
from okex_sdk_api.okex import futures_api as future

with open(o_path+"/json/accounts.json", 'r', encoding='UTF-8') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key = myokapi_info['api_key']
    seceret_key = myokapi_info['seceret_key']
    passphrase = myokapi_info['passphrase']
futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)

instrument = 'BTC-USD-200925'
# 记录okex期货下单 并发邮件


def bd():
    mail_text = ''  # 邮件内容
    sms_text = ''  # 短信内容
    qty_type = 0
    try:
        result = futureAPI.get_specific_position(instrument)
        # long_qty  short_qty 空仓数量
        # long_avg_cost  short_avg_cost 开仓平均价
        # long_settlement_price short_settlement_price  结算基准价
        my_future = result['holding'][0]  # 我的量化数据
        print()
        if my_future['long_qty'] == '0' and my_future['short_qty'] == '0':
            qty_type = 0  # 空仓
            mail_text = '空仓'
            sms_text = '记得看太阳下山'
        else:
            if my_future['long_qty'] == '0':
                mail_text = '{}平多套保。上次动作：{}开多'.format(
                    my_future['short_avg_cost'], my_future['long_avg_cost'])
                qty_type = 2  #
                sms_text = '今天乌云密布'
            elif my_future['short_qty'] == '0':
                mail_text = '{}平空开多。上次动作：{}开空'.format(
                    my_future['long_avg_cost'], my_future['short_avg_cost'])
                qty_type = 1  # 开多
                sms_text = '今天万里晴空'
            else:
                mail_text = '多空双开'
                qty_type = 4  # 多空双开
                sms_text = '记得看月亮'
        print(mail_text)
    except Exception as e:
        print("future_record.py -bd()出現异常:"，e）
    if mail_text != '':
        mail_result = tools.alert_mail_1('期货开单', mail_text, 2, sms_text)ß
        # 如果期货开单，则其他账户执行买入
        if mail_result and qty_type != 4:
            # take_order(qty_type)
            pass


'''
type
1:开多2:开空3:平多4:平空
order_type
4：市价委托
'''


def take_order(qty_type):
    try:
        account_list = tools.get_buy_account_list()
        for account in account_list:
            keyvalue, buy_api_key, buy_seceret_key, buy_passphrase, buy_instrument, order_size = account  # 拆包
            buy_futureAPI = future.FutureAPI(
                buy_api_key, buy_seceret_key, buy_passphrase, True)
            result = buy_futureAPI.get_specific_position(buy_instrument)
            buy_future = result['holding'][0]  # 该账户量化数据
            buy_result1, buy_result2 = '', ''
            if buy_future['long_qty'] == '0' and buy_future['short_qty'] == '0':
                # 如果持仓为空
                if qty_type != 0:
                    buy_result1 = buy_futureAPI.take_order(buy_instrument, str(
                        qty_type), '', size=order_size, order_type='4')
            elif (buy_future['long_qty'] == '0' and qty_type == 1) or (buy_future['short_qty'] == '0' and qty_type == 2):  # 目前开空
                buy_result1 = buy_futureAPI.take_order(buy_instrument, str(
                    qty_type), '', size=order_size, order_type='4')
                time.sleep(2)
                buy_result2 = buy_futureAPI.take_order(buy_instrument, str(
                    5-qty_type), '', size=order_size, order_type='4')
            elif (qty_type == 0 and (buy_future['long_qty'] == '0' or buy_future['short_qty'] == '0')):
                if buy_future['long_qty'] == '0':
                    buy_result2 = buy_futureAPI.take_order(
                        buy_instrument, '4', '', size=order_size, order_type='4')
                else:
                    buy_result2 = buy_futureAPI.take_order(
                        buy_instrument, '3', '', size=order_size, order_type='4')
            else:
                pass
            tools.warning(keyvalue, buy_result1, buy_result2, sep='\n')
            time.sleep(5)
    except Exception as e:
        print("future_record.py -take_order()出現异常:"，e)
        sms_text = '请查看异常天气'
        sms_result = sms_send.send(sms_text, True)


if __name__ == "__main__":
    bd()
