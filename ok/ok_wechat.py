import okex.futures_api as future
import okex.spot_api as spot
import okex.swap_api as swap
from utils import ms_sql as sql

ms = sql.MSSQL()

# itchat.auto_login(enableCmdQR=True)
#
#
# @itchat.msg_register(TEXT)
# def text_reply(msg):
#     if msg['FromUserName'] == '@efd311ea496fbfcd5b55ae8a164512845605463d6c5703cab311c0f8b4018f3a':
#         return '你是xxxx~'  # 可以对某人专门回复
#
#
# @itchat.msg_register(TEXT, isGroupChat=True)
# def text_reply(msg):
#     white_list = {
#         'bos': 'bos',
#     }

def job():
    inputval=input("请输入查询：")
    key = inputval.split('询')
    # key=msg['Text'].split('询')

    if(len(key)==2 and key[0]=='查'):
        keyvalue=key[1]
        account = ms.ExecQueryOne(
            "  select api_key,seceret_key,passphrase from tab_accounts where  keyvalue='" + keyvalue + "' ")
        if (account  is not None):
            api_key=str(account[0])
            seceret_key=str(account[1])
            passphrase=str(account[2])

            row = ms.ExecQueryOne(
                "select top 1 * from okex where  name='" + keyvalue + "' and DateDiff(dd,create_time,getdate())<=1 order by create_time asc ")
            lastday = '0'
            lastday_btc = '0.0'
            lastday_eth = '0.0'
            lastday_eos = '0.0'
            lastday_etc = '0.0'

            sys.exit(0)
            if (row is not None):
                lastday = str(row[1])
                lastday_btc = str(row[4])
                lastday_eth = str(row[5])
                lastday_eos = str(row[6])
                lastday_etc = str(row[7])

                print('' + keyvalue + ': ')

                spotAPI = spot.SpotAPI(api_key, seceret_key, passphrase, True)
                spotresult = spotAPI.get_coin_account_info('USDT')

                futureAPI = future.FutureAPI(api_key, seceret_key, passphrase, True)
                btc_amunt = futureAPI.get_coin_account('btc')
                etc_amunt = futureAPI.get_coin_account('etc')
                eth_amunt = futureAPI.get_coin_account('eth')
                eos_amunt = futureAPI.get_coin_account('eos')

                swapAPI = swap.SwapAPI(api_key, seceret_key, passphrase, True)
                btc_price = swapAPI.get_mark_price('BTC-USD-SWAP')['mark_price']
                etc_price = swapAPI.get_mark_price('ETC-USD-SWAP')['mark_price']
                eth_price = swapAPI.get_mark_price('ETH-USD-SWAP')['mark_price']
                eos_price = swapAPI.get_mark_price('EOS-USD-SWAP')['mark_price']

                # 查询价格
                btc = float(str(btc_price)) * float(str(btc_amunt['equity']))
                etc = float(str(etc_price)) * float(str(etc_amunt['equity']))
                eth = float(str(eth_price)) * float(str(eth_amunt['equity']))
                eos = float(str(eos_price)) * float(str(eos_amunt['equity']))
                all = str(eos + eth + btc + etc + float(str(spotresult['balance'])))

                # 盈利比率
                bfb = '%.2f%%' % ((float(all) - float(lastday)) / float(all) * 100)
                if (lastday == '0'):
                    bfb = '0%'


                res = keyvalue + ':\n当前币币账户USDT:' + spotresult['balance'] + '\n' + '当前合约账户btc:' + btc_amunt[
                    'equity'] + ';\n昨日' + lastday_btc + '\n' + '当前合约账户etc: ' + etc_amunt['equity']
                res = res + ';\n昨日' + lastday_etc + '\n' + '当前合约账户eth: ' + eth_amunt[
                    'equity'] + ';\n昨日' + lastday_eth + '\n' + '当前合约账户eos: ' + eos_amunt[
                          'equity'] + ';\n昨日' + lastday_eos + '\n账户总计USDT约: ' + all + ';\n昨日: ' + lastday + '\n' + '今日USDT本位盈利率' + bfb

                # return res
                print(res)
        else:
            print('查询口令错误')
            # return '查询口令错误'


# itchat.run(debug=True)
job()