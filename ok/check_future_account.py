import datetime
import time
import schedule
import sys
import os
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from utils import tools
from utils import ms_sql as sql
import okex_sdk_api.okex.swap_api as swap
import okex_sdk_api.okex.spot_api as spot
import okex_sdk_api.okex.futures_api as future

# 记录多个期货账户持仓检测
ms = sql.MSSQL()

def check(keyvalue):
    try:
        tools.time_print('多个期货账户持仓检测')
        account = tools.get_account_bykeyvalue(keyvalue)
        if(account is not None):
            # 如果账户不为空，说明该输入值存在一个账户
            api_key, seceret_key, passphrase, buy_instrument, order_size = account  # 拆包
            # 单个合约持仓信息
            # long_qty  short_qty 空仓数量
            # long_avg_cost  short_avg_cost 开仓平均价
            futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
            # buy_result = futureAPI.take_order(buy_instrument, '2','',size='2', order_type='4')
            # time.sleep(3)
            result = futureAPI.get_specific_position(buy_instrument)
            mail_text,text2='',''
            my_future = result['holding'][0]  # 我的量化数据
            if my_future['long_qty'] == '0' and my_future['short_qty']=='0':
                # 如果持仓为空，则该账户为开仓
                mail_text='{}账户{}未开仓'.format(keyvalue,buy_instrument)
            else:
                # 如果持仓不为空，判断是多还是空，输出持仓情况。
                if my_future['long_qty'] == '0':
                    mail_text = '{}账户目前在{}价格套保{}张'.format(
                        keyvalue, my_future['short_avg_cost'], my_future['short_qty'])
                else:
                    mail_text = '{}账户目前在{}价格开多{}张'.format(
                        keyvalue, my_future['long_avg_cost'], my_future['long_qty'])
            # 判断账户类型是否全仓
            margin_mode='全仓' if my_future['margin_mode']=='crossed' else '逐仓' # 三元运算符
            text2='，账户类型：{}，杠杆倍数：{}。'.format(margin_mode,my_future['leverage'])
            print(mail_text+text2)
            # 
            # 无法设置，api有bug  https://www.okex.me/docs/zh/#futures-leverage
            # "error_message":"instrument_id cannot be blank"
            # result12 = futureAPI.set_leverage('BTC-USD','10')
            # result11 = futureAPI.get_leverage('BTC-USD')
            # print(result11)
            # 
        else:
            # 如果不存在该输入账户，则输出所有账户持仓情况。
            account_list = tools.get_buy_account_list()
            for account in account_list:
                keyvalue, api_key, seceret_key, passphrase, buy_instrument, order_size = account  # 拆包
                futureAPI = future.FutureAPI(
                    api_key, seceret_key, passphrase, True)
                result = futureAPI.get_specific_position(buy_instrument)
                print(result)
                '''
                检查所有的账户对应取值是否正确，设置是否正确
                不正确的话 代码进行设置
                '''
                time.sleep(6)
    except Exception as e:
        print('记录多个期货账户持仓检测异常:', e)


if __name__ == "__main__":
    keyvalue = 'zt'
    # keyvalue=input("请输入查询：")
    
    check(keyvalue)
