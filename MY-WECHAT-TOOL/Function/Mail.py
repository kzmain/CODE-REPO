import json
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from smtplib import SMTP_SSL

import itchat

from System import Paths


class Mail:
    sender_mail = ""
    sender_smtp = ""
    sender_pswd = ""

    receiver_normal = ""
    receiver_special = ""

    sender_mail_key = "mail"
    sender_smtp_key = "smtp"
    sender_pswd_key = "pswd"

    receiver_normal_key = "normal"
    receiver_special_key = "special"

    def __init__(self):
        with open(os.path.join(Paths.PATH_FULL_SYS_LOCATION, "Config/auto_reply/sender.json"), "r") as file:
            sender_json = json.loads(file.read())
            self.sender_mail = sender_json[self.sender_mail_key]
            self.sender_pswd = sender_json[self.sender_pswd_key]
            self.sender_smtp = sender_json[self.sender_smtp_key]
        with open(os.path.join(Paths.PATH_FULL_SYS_LOCATION, "Config/auto_reply/receiver.json"), "r") as file:
            receiver_json = json.loads(file.read())
            self.receiver_normal = receiver_json[self.receiver_normal_key]
            self.receiver_special = receiver_json[self.receiver_special_key]

    def send_mail_normal(self, mail_title, mail_content):
        self.__send_mail(mail_title, mail_content, self.receiver_normal)

    def send_mail_special(self, mail_title, mail_content):
        self.__send_mail(mail_title, mail_content, self.receiver_special)

    def __send_mail(self, mail_title, mail_content, receiver):
        # ssl登录
        try:
            smtp = SMTP_SSL(self.sender_smtp)
            smtp.ehlo(self.sender_smtp)
            smtp.login(self.sender_mail, self.sender_pswd)
            # Setup message
            msg = MIMEText(mail_content, "plain", 'utf-8')
            msg["Subject"] = Header(mail_title, 'utf-8')
            msg["From"] = self.sender_mail
            msg["To"] = receiver
            # Send Message
            smtp.sendmail(self.sender_mail, receiver, msg.as_string())
            # Quit
            smtp.quit()
        except (smtplib.SMTPException, smtplib.SMTPServerDisconnected):
            itchat.send("邮件配置错误，无法联系到您邮箱，请检查配置", 'filehelper')
            return False

