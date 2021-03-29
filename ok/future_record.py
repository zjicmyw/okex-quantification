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

instrument = ['BTC-USD-210625','BTC-USD-210924']
last_mail_text = ['','']


# 记录okex期货下单 并发邮件


def bd(index):
    mail_text = ''  # 邮件内容
    sms_text = ''  # 短信内容
    qty_type = 0
    try:
        result = futureAPI.get_specific_position(instrument[index])
        # long_qty  short_qty 空仓数量
        # long_avg_cost  short_avg_cost 开仓平均价
        # long_settlement_price short_settlement_price  结算基准价
        my_future = result['holding'][0]  # 我的持仓数据
        res2 = futureAPI.get_fills(instrument[index], after='4096402419785729') # 我的订单数据
        # if __name__ == "__main__":
        #     pass
           
            # res2 = futureAPI.get_fills('BTC-USD-210326', after='4096402419785729')
            # print(res2[0][0]['price'],res2[0][0]['created_at'],res2[0][0]['side'])
        if len(res2[0])==0:
            print(instrument[index]+'暂无持仓')
        else:
            if my_future['long_qty'] == '0' and my_future['short_qty'] == '0':
                qty_type = 0  # 空仓
                mail_text = '空仓，{}：{}-{}'.format(
                    res2[0][0]['created_at'],res2[0][0]['side'],res2[0][0]['price'])
                sms_text = '记得看太阳下山'
            else:
                if my_future['long_qty'] == '0':
                    mail_text = '当前持仓{}空。上次动作：{}：{}-{}'.format(
                        my_future['short_avg_cost'], res2[0][0]['created_at'],res2[0][0]['side'],res2[0][0]['price'])
                    qty_type = 2  # 开空
                    sms_text = '今天乌云密布'
                elif my_future['short_qty'] == '0':
                    mail_text = '当前持仓{}多。上次动作：{}：{}-{}'.format(
                        my_future['long_avg_cost'], res2[0][0]['created_at'],res2[0][0]['side'],res2[0][0]['price'])
                    qty_type = 1  # 开多
                    sms_text = '今天万里晴空'
                else:
                    mail_text = '多空双开，当前持仓{}多，{}空。上次动作：{}：{}-{}'.format(
                        my_future['long_avg_cost'],my_future['short_avg_cost'], res2[0][0]['created_at'],res2[0][0]['side'],res2[0][0]['price'])
                    qty_type = 4  # 多空双开
                    sms_text = '记得看月亮'
            mail_text = instrument[index]+mail_text
            tools.time_print(mail_text)
    except Exception as e:
        print("future_record.py -bd()出現异常:",e)
    if mail_text != '':
        if last_mail_text[index] == mail_text:
            print('持仓无变化')
        else:
            last_mail_text[index] = mail_text
            sms_send.send_wecaht(sms_text,mail_text)
    
            
            


'''
type
1:开多2:开空3:平多4:平空
order_type
4：市价委托
'''

if __name__ == "__main__":
    for index in [0,1]:
        bd(index)
