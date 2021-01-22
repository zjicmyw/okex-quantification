import requests
import json

with open("json/accounts.json", 'r', encoding='UTF-8') as load_f:
    content = json.load(load_f)
    sms_wrong_config = content['sms_wrong_config']
    sms_normal_config = content['sms_normal_config']
    sms_info = content['sms_info']
    sms_url = sms_info['sms_url']
    sms_data = sms_info['sms_data']
    phone = sms_info['phone']


def send(content, is_error):
    sms_data['i'] = content
    if is_error:
        sms_data['p'] = phone
    res = requests.get(url=sms_url, params=sms_data)
    return(res.text)


def send_wrong_sms():
    r = requests.post("https://api.mysubmail.com/message/send",
                      data=sms_wrong_config)
    print(r)

def send_normal_sms():
    r = requests.post("https://api.mysubmail.com/message/send",
                      data=sms_normal_config)
    print(r)

def send_wecaht(title,desp):
    r = requests.get("https://sc.ftqq.com/SCU153099T7981d7e4bd60158a48b6f9f9f37e3da9600958eaaef11.send?text={}&desp={}".format('趋势提醒：'+title,desp))
    print(r)
