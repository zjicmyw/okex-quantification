# coding=utf-8
import json
import sys
import os
# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from okex_sdk_api.okex import spot_api as spot
from utils import tools

with open(o_path+"/json/accounts.json",'r') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key = myokapi_info['api_key']
    seceret_key = myokapi_info['seceret_key']
    passphrase = myokapi_info['passphrase']

instrument='BTC-USDT'

spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)

# 记录okexBTC现货量化下单 并发邮件

def bd():
    tools.time_print('现货检测')
    mail_text = ''  # 邮件内容

    try:
        result = spotAPI.get_orders_list(state='2', instrument_id=instrument)

        # side	String	buy 或 sell
        # price_avg	String	成交均价

        my_last_spot1 = result[0][0]  # 我的最新一次下单数据
        my_last_spot2 = result[0][1]  # 我的最新二次下单数据

        mail_text = '最新一次时间:{0},动作：{1}，成交均价{2};'.format(
            my_last_spot1['created_at'], my_last_spot1['side'], my_last_spot1['price_avg'])
        mail_text += '上两次时间:{0},动作：{1}，成交均价{2};'.format(
            my_last_spot2['created_at'], my_last_spot2['side'], my_last_spot2['price_avg'])
    except Exception as e:
        print("spot_record.py出現异常:", e)
        
    if mail_text != '':
        tools.alert_mail_1('现货开单', mail_text, 1)

if __name__ == "__main__":
    bd()

