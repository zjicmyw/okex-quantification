import datetime
import time
import sys
import os
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path)  # 添加自己指定的搜索路径
import okex_sdk_api.okex.futures_api as future
import okex_sdk_api.okex.spot_api as spot
import okex_sdk_api.okex.swap_api as swap
from utils import ms_sql as sql
from utils import tools
# 记录多个量化账户量化资金变化
ms = sql.MSSQL()


def okex():
    try:
        tools.time_print('多个量化账户量化资金检测')
        zh = ms.ExecQueryALL(
            "select keyvalue from tab_accounts where status =2")
        create_time = datetime.datetime.strftime(
                    datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        for i in zh:
            keyvalue = list(i)[0]
            account = ms.ExecQueryOne(
                "  select api_key,seceret_key,passphrase,order_instrument_id from tab_accounts where  keyvalue='" + keyvalue + "' ")
            if (account is not None):
                api_key = str(account[0])
                secret_key = str(account[1])
                passphrase = str(account[2])
                instrument_id = str(account[3])

                print('' + keyvalue + ': ',instrument_id)
               
                 # swap api test
                swapAPI = swap.SwapAPI(
                    api_key, secret_key, passphrase, True)

                if instrument_id == 'None':
                    result_get_accounts = swapAPI.get_accounts()

                    eos_equity = result_get_accounts['info'][5]['equity']
                    bsv_equity = result_get_accounts['info'][7]['equity']
                    eth_usd_equity = result_get_accounts['info'][11]['equity']
                    eos_usd_equity = result_get_accounts['info'][14]['equity']
                    total_usd_value = float(
                        eth_usd_equity)+float(eos_usd_equity)

                    eos_price = swapAPI.get_mark_price(
                        'EOS-USD-SWAP')['mark_price']
                    bsv_price = swapAPI.get_mark_price(
                        'BSV-USD-SWAP')['mark_price']

                    eos_value = float(eos_equity)*float(eos_price)
                    bsv_value = float(bsv_equity)*float(bsv_price)
                    total_value = eos_value+bsv_value

                    tab_price_id = 0

                    sql0 = "insert into tab_price (eos_price,bsv_price,create_time) values('%s','%s','%s')" % (
                        eos_price, bsv_price, create_time)
                    ms.ExecNonQuery(sql0)
                    # print(sql0)

                    sql1 = "insert into tab_okex_account_swapbytoken (keyvalue,eos_equity,bsv_equity,eos_value,bsv_value,total_value,tab_price_id,create_time) values('%s','%s','%s',%d,%d,%d,%d,'%s')" % (
                        keyvalue, eos_equity, bsv_equity, eos_value, bsv_value, total_value, tab_price_id, create_time)
                    ms.ExecNonQuery(sql1)
                    # print(sql1)

                    sql2 = "insert into tab_okex_account_swapbydoller (keyvalue,eth_usd_equity,eos_usd_equity,total_value,create_time) values('%s','%s','%s',%d,'%s')" % (
                        keyvalue, eth_usd_equity, eos_usd_equity, total_usd_value, create_time)
                    ms.ExecNonQuery(sql2)
                    # print(sql2)
                elif instrument_id == 'ETH-USD-SWAP':
                    result_get_accounts = swapAPI.get_coin_account(instrument_id)
                    eth_usd_equity = result_get_accounts['info']['equity']
                    # print(result_get_accounts)
                    sql1 = "insert into tab_swap_one_token (keyvalue,instrument_id,equity,create_time) values('%s','%s','%s','%s')" % (
                        keyvalue, instrument_id, eth_usd_equity, create_time)
                    ms.ExecNonQuery(sql1)
                    # print(sql1)

                time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(2)


if __name__ == "__main__":
    okex()
