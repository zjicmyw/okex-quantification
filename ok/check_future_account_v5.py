import json
import time
import sys
import os
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from utils import tools,sms_send
import okex_sdk_api.okex.account_api as account
import okex_sdk_api.okex.futures_api as future
import okex_sdk_api.okex.spot_api as spot
import okex_sdk_api.okex.swap_api as swap

last_mail_text = {
    'SPOT': '',
    'MARGIN': '',
    'SWAP': '',
    'FUTURES': '',
    'OPTION': ''
}
last_usdt_balance = 0

with open(o_path+"/json/accounts.json", 'r', encoding='UTF-8') as load_f:
    myokapi_info = json.load(load_f)['myokapi-v5']
    api_key = myokapi_info['api_key']
    secret_key = myokapi_info['seceret_key']
    passphrase = myokapi_info['passphrase']


def okex_v5():
    try: 
        global last_mail_text,last_usdt_balance
        mail_text = {}
        text = ''
        sms_text = ''
        accountAPI = account.AccountAPI(api_key, secret_key, passphrase, False)


        # 现货版本 

        last_order_history = accountAPI.get_last_order_history()
        if last_order_history['code'] == '0':
            # print(last_order_history)
            # print(len(last_order_history['data']))
            if len(last_order_history['data'])==0:
                 tools.warning('持仓无变化')
            else:
                data = last_order_history['data'][0]
                uTime = timestamp_to_str(int(data['fillTime']))

                mail_text['SPOT'] = '{}:{}-开单：{}-{},{}。'.format(
                                    uTime, data['instId'],data['side'],data['fillPx'], data['accFillSz'])

                if last_mail_text == mail_text:
                    tools.warning('持仓无变化')
                else:
                    last_mail_text = mail_text
                    tools.warning(str(last_mail_text))
                    sms_send.send_wecaht(sms_text, mail_text)
                    sms_send.send_to_wecom(str(mail_text))
            
            
        else:
            print('获取出错'+last_order_history)
            
            
            
            
      
        # 期货版本
    

        # if result['code'] != '0':
        #     for position in result['data']:
        #         instType = position['instType']
        #         instId = position['instId']
        #         posSide = position['posSide']
        #         liqPx = position['liqPx']
        #         last = position['last']
        #         uTime = timestamp_to_str(int(position['uTime']))
        #         context = '{}:{}-{}-开单：{}-{}。开仓后，清算价变为{}。'.format(
        #             uTime, instType, instId, posSide, last, liqPx)
        #         sms_text = '量化'

        #         if instType == 'FUTURES':
        #             text = text + context
        #         else:
        #             text = context

        #         mail_text[instType] = text

        #     if last_mail_text == mail_text:
        #         tools.warning('持仓无变化')
        #     else:
        #         last_mail_text = mail_text
        #         tools.warning(str(last_mail_text))
        #         # sms_send.send_wecaht(sms_text, mail_text)
        #         # sms_send.send_to_wecom(str(mail_text))

        """
        instType	String	产品类型
        SPOT：币币
        MARGIN：币币杠杆
        SWAP：永续合约
        FUTURES：交割合约
        OPTION：期权
    
        instId	String	产品ID

        posSide	String	持仓方向
        long：双向持仓多头
        short：双向持仓空头
        net：单向持仓（交割/永续/期权：pos为正代表多头，pos为负代表空头。币币杠杆：posCcy为交易货币时，代表多头；posCcy为计价货币时，代表空头。）


        liqPx	String	预估强平价
        不适用于跨币种保证金模式下交割/永续的全仓
        不适用于期权


        last	String	最新成交价


        uTime	String	最近一次持仓更新时间，Unix时间戳的毫秒数格式，如 1597026383085
        """

    except Exception as e:
        print('记录期货账户持仓检测异常:', str(e))


def timestamp_to_str(timeStamp):
    timeStamp = float(timeStamp/1000)
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


if __name__ == "__main__":
    okex_v5()
