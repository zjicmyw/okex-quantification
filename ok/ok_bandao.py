import json
import datetime
import sys
import os
# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
import okex.futures_api as future
from common import tools


with open("database/accounts.json",'r') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key=myokapi_info['api_key']
    seceret_key=myokapi_info['seceret_key']
    passphrase=myokapi_info['passphrase']
futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)


# 记录okex期货下单 并发邮件
def bd():
    nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('期货检测：'+'\033[0;34;40m\t' + nowtime + ': \033[0m')
    mail_text='' # 邮件内容

    try:
        result = futureAPI.get_specific_position('BTC-USD-200327') 
        # long_qty  short_qty 空仓数量
        # long_avg_cost  short_avg_cost 开仓平均价 
        # long_settlement_price short_settlement_price  结算基准价      

        my_future=result['holding']# 我的量化数据
        if my_future[0]['long_qty']=='0':
            mail_text=my_future[0]['short_avg_cost']+'开空。上次动作：'+my_future[0]['long_avg_cost']+'开多，'+my_future[0]['long_settlement_price']+'平多'
        else:
            mail_text=my_future[0]['long_avg_cost']+'开多。上次动作：'+my_future[0]['long_avg_cost']+'开空，'+my_future[0]['long_settlement_price']+'平空'
    except Exception as e:
        print("ok_baodao.py出現异常:", e)
        
    if mail_text != '':
        tools.alert_mail('期货开单', mail_text, 2)

if __name__ == "__main__":
    bd()
