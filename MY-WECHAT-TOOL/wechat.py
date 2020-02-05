import time

import itchat
from itchat.content import *

from Function.AutoReply import AutoReply
from Function.Mail import Mail
from System.Sys import Sys
from file_helper import file_helper as fh


# 用于自动回复，封装好的装饰器，当接收到的消息是Text，即文字消息
@itchat.msg_register(TEXT)
def text_reply(msg):
    if Sys.my_uid == msg.FromUserName:
        AutoReply.last_time = float(time.time())
        if msg.ToUserName == "filehelper":
            if fh.fh_func is not None:
                fh.fh_continue_previous_task(msg)
            else:
                argv = fh.fh_check_task(msg)
                task = argv.pop()
                fh.fh_start_new_task(task, argv)
        else:
            if msg.ToUserName in AutoReply.history_message.keys():
                AutoReply.clear_user_history_message(msg.ToUserName)
    else:
        AutoReply.text_reply(msg)


# 用于自动回复，封装好的装饰器，当接收到的消息是Text 且@ 回复
@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if Sys.my_uid == msg.FromUserName:
        AutoReply.last_time = float(time.time())
        if msg.ToUserName in AutoReply.history_message.keys():
            AutoReply.clear_user_history_message(msg.ToUserName)
    else:
        AutoReply.text_reply(msg, True)


if __name__ == '__main__':
    try:
        # enable cmd qr参数是用于在命令行上生成二维码，用于linux服务器
        itchat.auto_login(enableCmdQR=Sys.choose_console_color())

        Sys.my_uid = itchat.get_friends(update=True)[0]["UserName"]
        itchat.run(debug=True)
    except itchat:
        mail = Mail()
        mail.send_mail_special("Wechat看守系统消息", "你家炸了！")
        del mail
