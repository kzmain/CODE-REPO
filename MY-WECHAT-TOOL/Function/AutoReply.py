import json
import os
import random
import smtplib
import time
import threading
import uuid

import itchat

from Function.Mail import Mail
from System import Paths


class AutoReply:
    wait_min = None
    bot_name = None
    contact_method = None
    last_time = time.time()

    status = True
    check_thread = None

    history_message = {}
    first_prefix = None
    other_prefix = None
    first_flag = True
    mail_title = 'Wechat %s 的信息'
    modal = ["哇哦，这样嘛？！", "妈耶！", "嘿嘿～。", "啦啦啦~", "噗～", "嘻嘻～", "矮油～"]
    sentences = ["（悄悄记下来通知主人）📝",
                 "折个纸飞机通知主人（咻～）✈️",
                 "（哼哧，哼哧。腿跑断了也要通知到主人）🏃️",
                 "开车通知主人。（嗯，通向幼儿园的车，请刷学生卡）🚌",
                 "开车通知主人。（北京市第三交通委提醒您，喝车不开酒）🚘",
                 "搭高铁通知主人！（chua, chua, chua 好快呦）🚄",
                 "就算搭火箭也要通知到主人！（10, 9, 8, 7, 6,....）🚀",
                 "嘀叭叭，滴叭叭，嘀嘀叭叭，开着快乐家家车，找主人去～🚍",
                 "那个电车好酷哦～搭电车去找主人。(当～当～当～)🚋",
                 "干了这杯酒找主人去。（咕嘟～咕嘟～）🍺",
                 "库洛里多创造的库洛牌啊，请你舍弃旧形象，重新改变，以你的新主人小开开之名命令你，把这个消息送给我主人！（砰～）🎩"]

    @staticmethod
    def text_reply(msg, is_group=False):
        if not AutoReply.status:
            return
        AutoReply.__pre_get_bot_config()
        AutoReply.__pre_get_contact_method()
        uname = msg.User["RemarkName"] if msg.User["RemarkName"] != "" else msg.User["NickName"]
        special_string = ""
        if "⭐️" in uname:
            special = True
            special_string = "你好，你是主人的星标朋友，优先直接通知到主人."
        else:
            special = False
        uid = msg.User["UserName"]
        if uid not in AutoReply.history_message.keys():
            prefix = AutoReply.other_prefix + AutoReply.first_prefix
            AutoReply.history_message[uid] = {"UNAME": uname, "MESSAGES": []}
            AutoReply.first_flag = True
        else:
            AutoReply.history_message[uid]["UNAME"] = uname
            prefix = AutoReply.other_prefix
            AutoReply.first_flag = False
        if float(float(time.time() - AutoReply.last_time) / 60) > AutoReply.wait_min:
            try:
                mail_content = msg.Content
                mail_title = AutoReply.mail_title % uname
                mail = Mail()
                if special:
                    mail.send_mail_special(mail_title, mail_content)
                else:
                    mail.send_mail_normal(mail_title, mail_content)
                random.seed(uuid.uuid4())
                if AutoReply.first_flag:
                    sentence = AutoReply.sentences[random.randint(0, len(AutoReply.sentences) - 1)]
                    if not is_group:
                        contact = ""
                        if AutoReply.contact_method is not None:
                            contact = "，或请直接联系 %s" % AutoReply.contact_method
                        itchat.send(prefix + "主人已长时间离开微信，我替他在看微信。您的留言我将通过邮件通知他%s。" % contact, uid)
                        itchat.send(AutoReply.other_prefix + "诶，有消息。" + sentence, uid)
                        if special_string != "":
                            itchat.send(AutoReply.other_prefix + special_string, uid)
                    else:
                        itchat.send(AutoReply.other_prefix + "已邮件通知主人，或您可以在私聊中获取电话号码直接电话联系。", uid)
                else:
                    if not is_group:
                        modal = AutoReply.modal[random.randint(0, len(AutoReply.modal)) - 1]
                        sentence = AutoReply.sentences[random.randint(0, len(AutoReply.sentences) - 1)]
                        if special_string != "":
                            ss = "(" + special_string + ")"
                        else:
                            ss = ""
                        itchat.send(prefix + ss + modal + sentence, uid)
                    else:
                        itchat.send(AutoReply.other_prefix + "已邮件通知主人，或您可以在私聊中获取电话号码直接电话联系。", uid)
            except (TypeError, smtplib.SMTPServerDisconnected, smtplib.SMTPAuthenticationError, smtplib.SMTPException):
                itchat.send(AutoReply.other_prefix + "系统bug无法邮件通知主人，或许您可以直接电话联系。", uid)
        else:
            AutoReply.history_message[uid]["MESSAGES"].append(msg.Content)
            if AutoReply.check_thread is None:
                AutoReply.check_thread = threading.Thread(target=AutoReply.__check_update, args=())
                AutoReply.check_thread.start()

    @staticmethod
    def clear_all_history_message(empty_list):
        AutoReply.history_message = {}
        itchat.send("(System) History message cleared!", 'filehelper')
        len(empty_list)

    @staticmethod
    def clear_user_history_message(uid):
        AutoReply.history_message[uid]["MESSAGES"].clear()

    @staticmethod
    def stop_auto_reply():
        if AutoReply.check_thread is not None:
            AutoReply.check_thread.join()
        AutoReply.history_message = {}
        AutoReply.status = False

    @staticmethod
    def start_auto_reply():
        AutoReply.status = True

    @staticmethod
    def __pre_get_bot_config():
        if AutoReply.wait_min is None:
            with open(os.path.join(Paths.PATH_FULL_SYS_LOCATION, "Config/auto_reply/bot.json"), "r") as file:
                try:
                    bot_json = json.loads(file.read())
                    AutoReply.wait_min = bot_json["wait_min"]
                    AutoReply.bot_name = bot_json["name"]
                    if AutoReply.wait_min < 0:
                        AutoReply.wait_min = 10
                        itchat.send("自动回复等待时间配置错误，设置默认等待时间10分钟", 'filehelper')
                except (TypeError, FileNotFoundError):
                    AutoReply.wait_min = 10
                    AutoReply.bot_name = "小机器人"
                    itchat.send("自动回复等待时间配置错误，设置默认等待时间10分钟", 'filehelper')

                AutoReply.first_prefix = "我是%s，" % AutoReply.bot_name
                AutoReply.other_prefix = "(%s)" % AutoReply.bot_name

    @staticmethod
    def __pre_get_contact_method():
        if AutoReply.contact_method is None:
            with open(os.path.join(Paths.PATH_FULL_SYS_LOCATION, "Config/auto_reply/contact.json"), "r") as file:
                try:
                    AutoReply.contact_method = ""
                    contacts = json.loads(file.read())
                    for key, value in contacts.items():
                        if AutoReply.contact_method != "":
                            AutoReply.contact_method += ","
                        AutoReply.contact_method += key + " : " + value
                except FileNotFoundError:
                    AutoReply.contact_method = None

    @staticmethod
    def __check_update():
        while True:
            wait_sec = float(float(time.time() - AutoReply.last_time))
            if wait_sec > AutoReply.wait_min * 60:
                wait_sec = AutoReply.wait_min * 60
            time.sleep(wait_sec + 0.001)
            last_now_len = float(float(time.time() - AutoReply.last_time) / 60)
            if last_now_len > AutoReply.wait_min:
                if len(AutoReply.history_message) > 0:
                    for uid, uid_dict in AutoReply.history_message.items():
                        content = ""
                        user_name = uid_dict["UNAME"]
                        if "⭐️" in user_name:
                            special = True
                            special_string = "你好，你是主人的星标朋友，优先直接通知到主人."
                        else:
                            special = False
                            special_string = ""
                        title = AutoReply.mail_title % uid_dict["UNAME"]
                        if len(uid_dict["MESSAGES"]) > 0:
                            itchat.send(
                                AutoReply.other_prefix + AutoReply.first_prefix + "主人已长时间离开微信，我替他在看微信。您的留言我将通过邮件通知他！",
                                uid)
                            for message in uid_dict["MESSAGES"]:
                                if content == "":
                                    content += ("%s" % message)
                                else:
                                    content += ("\n%s" % message)
                            try:
                                mail = Mail()

                                random.seed(uuid.uuid4())
                                sentence = AutoReply.sentences[random.randint(0, len(AutoReply.sentences) - 1)]
                                if special:
                                    mail.send_mail_special(title, content)
                                    sentence = AutoReply.other_prefix + "(" + special_string + ")" + sentence
                                else:
                                    mail.send_mail_normal(title, content)
                                    sentence = AutoReply.other_prefix + sentence
                                itchat.send(sentence, uid)

                            except (smtplib.SMTPException, smtplib.SMTPServerDisconnected):
                                itchat.send(AutoReply.other_prefix + "系统bug无法邮件通知主人，或许您可以直接电话联系。", uid)
                            uid_dict["MESSAGES"].clear()
