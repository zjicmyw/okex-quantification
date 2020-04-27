import requests
import json

with open("json/accounts.json", 'r') as load_f:
    sms_info = json.load(load_f)['sms_info']
    sms_url = sms_info['sms_url']
    sms_data = sms_info['sms_data']
    phone=sms_info['phone']


def send(content,is_error=False):
    sms_data['i'] = content
    if is_error:
        sms_data['p'] = phone
    res = requests.get(url=sms_url, params=sms_data)
    return(res.text)
