import itchat
from tuling import get_response
from itchat.content import *



itchat.auto_login(hotReload=True)

@itchat.msg_register(TEXT)
def text_reply(msg):
    print(msg)
    if msg['FromUserName'] == '@efd311ea496fbfcd5b55ae8a164512845605463d6c5703cab311c0f8b4018f3a':
        return '你是xxxx~'  #可以对某人专门回复
    elif msg['Text'] == '01':
        return '你好，我是！'
    else:
        return get_response(msg['Text'])

@itchat.msg_register(TEXT, isGroupChat = True)
def text_reply(msg):
    print(msg)
    white_list = {
        'pmcaff 专家群':'@@2b915b714a0e65fe93bb0b94dfc80156db79334ff9fda274ba08ae7638dd7cb6',
        '葫芦娃群':'@@90b2ad91b1c33967d6d0723217b6084ed0607c7b627f8a87e53d4e8b802ff1ed',
        }
    if msg['FromUserName'] in white_list.values():
        return get_response(msg['Text'])

itchat.run(debug=True)