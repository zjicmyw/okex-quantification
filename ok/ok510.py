import okex.futures_api as future
import okex.spot_api as spot
import okex.swap_api as swap
from utils import ms_sql as sql
import schedule
import time
import datetime

# 记录所有币扶量化资金变化
ms = sql.MSSQL()

# def job():
#    print("I'm working...")
# schedule.every(2).seconds.do(job)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("19:10").do(job)
# schedule.every(5).to(10).days.do(job)
# schedule.every().wednesday.at("19:10").do(job)
#
# while True:
#    schedule.run_pending()
#     # 每隔10秒检测一次
#    time.sleep(6)

# keyvalue=input("请输入查询：")

def okex():
    try:
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('\033[0;34;40m\t' + nowtime + ': \033[0m')
        zh = ms.ExecQueryALL(
                "  select keyvalue from tab_accounts where status =1")

        if __name__ == '__main__':
            for i in zh:
                keyvalue = list(i)[0]
                account = ms.ExecQueryOne(
                    "  select api_key,seceret_key,passphrase from tab_accounts where  keyvalue='" + keyvalue + "' ")
                if (account is not None):
                    api_key = str(account[0])
                    seceret_key = str(account[1])
                    passphrase = str(account[2])
                    row = ms.ExecQueryOne(
                        "select top 1 * from okex where  name='" + keyvalue + "' and DateDiff(dd,create_time,getdate())=1 order by create_time asc ")
                    # print(row)
                    lastday = '0'
                    lastday_btc='0.0'
                    lastday_eth='0.0'
                    lastday_eos='0.0'
                    lastday_etc='0.0'
                    if (row is not None):
                        lastday = str(row[1])
                        lastday_btc = str(row[4])
                        lastday_eth = str(row[5])
                        lastday_eos = str(row[6])
                        lastday_etc = str(row[7])


                    # sys.exit(0)
                    # print('\033[0;34;40m\t' + lastday + ': \033[0m')
                    print('' + keyvalue + ': ')
                    spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
                    spotresult = spotAPI.get_coin_account_info('USDT')
                    # future api test
                    futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
                    # futureresult_get_accounts = futureAPI.get_accounts()
                    # # print('当前合约账户'+json.dumps(futureresult_get_accounts.info))
                    # if(futureresult_get_accounts['info'].__contains__('btc')):
                    #     print('当前合约账户btc: '+futureresult_get_accounts['info']['btc']['equity'])
                    # if (futureresult_get_accounts['info'].__contains__('etc')):
                    #     print('当前合约账户etc: '+futureresult_get_accounts['info']['etc']['equity'])
                    # if (futureresult_get_accounts['info'].__contains__('eth')):
                    #     print('当前合约账户eth: '+futureresult_get_accounts['info']['eth']['equity'])
                    # if (futureresult_get_accounts['info'].__contains__('eos')):
                    #     print('当前合约账户eos: '+futureresult_get_accounts['info']['eos']['equity'])

                    btc_amunt = futureAPI.get_coin_account('btc')
                    etc_amunt = futureAPI.get_coin_account('etc')
                    eth_amunt = futureAPI.get_coin_account('eth')
                    eos_amunt = futureAPI.get_coin_account('eos')

                    # futureresult_get_position = futureAPI.get_position()
                    # print('当前合约账户持仓:' + json.dumps(futureresult_get_position['holding'][0][0]))

                    ####
                    # futureresult_get_order_list1 = futureAPI.get_order_list(6, '', '', '', 'ETH-USD-190329')
                    # futureresult_get_order_list2 = futureAPI.get_order_list(7, '', '', '', 'ETH-USD-190329')
                    #
                    # print('未完成:' + json.dumps(futureresult_get_order_list1))
                    # print('已完成:' + json.dumps(futureresult_get_order_list2))
                    # sys.exit(0)
                    #
                    ####
                    # print('当前合约账户持仓'+json.dumps(futureresult_get_position['holding'][0][0]))

                    # swap api test
                    swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)
                    btc_price = swapAPI.get_mark_price('BTC-USD-SWAP')['mark_price']
                    etc_price = swapAPI.get_mark_price('ETC-USD-SWAP')['mark_price']
                    eth_price = swapAPI.get_mark_price('ETH-USD-SWAP')['mark_price']
                    eos_price = swapAPI.get_mark_price('EOS-USD-SWAP')['mark_price']
                    btc = float(str(btc_price)) * float(str(btc_amunt['equity']))
                    etc = float(str(etc_price)) * float(str(etc_amunt['equity']))
                    eth = float(str(eth_price)) * float(str(eth_amunt['equity']))
                    eos = float(str(eos_price)) * float(str(eos_amunt['equity']))
                    all = str(eos + eth + btc + etc + float(str(spotresult['balance'])))

                    # ms.ExecNonQuery(newsql.encode('utf-8'))
                    # newsql = "insert into okex (usdt,name) values('" + all + "','" + keyvalue + "')"
                    # print(newsql)
                    #
                    # ms.ExecNonQuery(newsql)
                    # newsql = "insert into okex (usdt,name,btc,eth,eos,etc) values('" + all + "','" + keyvalue + "','" + btc_amunt['equity'] + ",'" + eth_amunt['equity'] + ",'" + eos_amunt['equity'] + ",'" + etc_amunt['equity'] + "')"



                    newsql = "insert into okex (usdt,name,btc,eth,eos,etc) values('" + all + "','" + keyvalue + "','" + btc_amunt[
                        'equity'] + "','" + eth_amunt['equity'] + "','" + eos_amunt['equity'] + "','" + etc_amunt['equity'] + "')"
                    ms.ExecNonQuery(newsql)

                    bfb = '%.2f%%' % ((float(all) - float(lastday)) / float(all) * 100)
                    if (lastday == '0'):
                        bfb = '0%'

                    res = keyvalue + ':\n当前币币账户USDT:' + spotresult['balance'] + '\n' + '当前合约账户btc:' + btc_amunt[
                        'equity'] + ';昨日'+lastday_btc+'\n' + '当前合约账户etc: ' + etc_amunt['equity']
                    res = res +';昨日'+lastday_etc+ '\n' + '当前合约账户eth: ' + eth_amunt['equity'] +';昨日'+lastday_eth+  '\n' + '当前合约账户eos: ' + eos_amunt[
                        'equity'] +';昨日'+lastday_eos+ '\n账户总计USDT约: ' + all + ';昨日: ' + lastday + '\n' + '今日USDT本位盈利率' + bfb

                    print(res)
                    time.sleep(10)
    except Exception as e:
        newsql = "insert into tab_send_email (address_to,mail_subject,mail_text) values('e7lian@qq.com','okex脚本出现问题'+'"+nowtime+"','"+str(e)+"')"
        ms.ExecNonQuery(newsql)
        time.sleep(10)

okex()
schedule.every(2).hours.do(okex)


while True:
   schedule.run_pending()
    # 每隔60秒检测一次
   time.sleep(60*1)
