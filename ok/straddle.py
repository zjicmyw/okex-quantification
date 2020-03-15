import json
import sys
import os
# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
from okex import spot_api as spot
from okex import futures_api as future
from common import tools

with open("json/accounts.json",'r') as load_f:
    myokapi_info = json.load(load_f)['myokapi']
    api_key=myokapi_info['api_key']
    seceret_key=myokapi_info['seceret_key']
    passphrase=myokapi_info['passphrase']

spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)

# 期现套利
# 记录okex期货出现溢价 并发邮件
def straddle():
    tools.time_print('溢价检测')
    mail_text = ''

    all_spot_ticker = spotAPI.get_ticker()  # get_ticker 获取全部ticker信息
    future_list = ['BTC-USDT', 'LTC-USDT', 'ETH-USDT', 'EOS-USDT', 'XRP-USDT', 'ETC-USDT', 'BCH-USDT',
                          'BSV-USDT']
    ticker_list = []
    for value in all_spot_ticker:
        if value['instrument_id'] in future_list:
            ticker_list.insert(len(ticker_list), {'name': value['instrument_id'][0:-1],
                                                  value['instrument_id'][0:-1]: value['last']})
    # best_ask 卖一价  last 最新成交价

    # print(ticker_list)
    # [{'name': 'ETH-USD', 'ETH-USD': '128.6'}, {'name': 'BTC-USD', 'BTC-USD': '5353.4'}, {'name': 'LTC-USD', 'LTC-USD': '35.44'}, {'name': 'ETC-USD', 'ETC-USD': '4.62'}, {'name': 'XRP-USD', 'XRP-USD': '0.1521'}, {'name': 'EOS-USD', 'EOS-USD': '2.014'}, {'name': 'BCH-USD', 'BCH-USD': '170.64'}, {'name': 'BSV-USD', 'BSV-USD': '118.59'}]
    

    all_future_ticker = futureAPI.get_ticker()
    for item in ticker_list:
        for future_ticker in all_future_ticker:
            if item['name'] in future_ticker['instrument_id'] and 'USDT' not in future_ticker['instrument_id']:
                item[future_ticker['instrument_id']] = future_ticker['last']
                rate = (float(future_ticker['last']) / float(item[item['name']]) * 100 - 100)
                item[future_ticker['instrument_id'] + '溢价'] = '%.2f' % rate + '%'
                if (rate > 4 or rate < -5) and ('200626' in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '次季溢价:' + str('%.2f' % rate + '%')
                elif (rate > 1.6 or rate < -2) and ('200327' in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '季度溢价:' + str('%.2f' % rate + '%')
                elif (rate > 0.8 or rate < -1) and ('200327' not in future_ticker['instrument_id']) and ('200626' not in future_ticker['instrument_id']):
                    mail_text = mail_text + '\r\n' + future_ticker['instrument_id'] + '周溢价:' + str('%.2f' % rate + '%')
    # [{'name': 'ETH-USD', 'ETH-USD': '171.78', 'ETH-USD-190517': '170.476', 'ETH-USD-190517溢价': '-0.76%', 'ETH-USD-190628': '171.191', 'ETH-USD-190628溢价': '-0.34%', 'ETH-USD-190510': '170.634', 'ETH-USD-190510溢价': '-0.67%'}]
    # print(ticker_list)
    if __name__ == "__main__":
        print(mail_text)
        sys.exit(0)

    if mail_text != '':
        tools.alert_mail_1('溢价检测', mail_text, 3)
    
if __name__ == "__main__":
    straddle()


