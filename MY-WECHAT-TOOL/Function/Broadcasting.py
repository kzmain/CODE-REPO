import collections
import copy
import re

import itchat

from System.Sys import Sys


class Broadcasting:
    content = ""

    udict_fin = {}
    udict_all = {}

    except_list = []
    only_list = []
    add_list = []

    wrong_time = 0

    prefix = "(群发模式)"
    warn_wrong_input = prefix + "非法输入，满三次错误以后将退出群发模式。或输入\"n\"直接退出"
    warn_wrong_number = prefix + "数字输入错误%s"
    warn_exit = prefix + "非法输入，第三次！退出群发模式！"
    warn_no_receiver = prefix + "没有更多符合的收件人了，退出群发模式！"

    info_exit = prefix + "群发模式已退出。"
    info_remove = prefix + "已移除：  %s"

    def broadcasting_prepare(self, content_list):
        if len(content_list) == 0:
            return "FALSE"
        self.content = content_list.pop()

        users_dict = itchat.get_friends(update=True)
        for user in users_dict:
            self.udict_fin[user["UserName"]] = user["RemarkName"] if user["RemarkName"] != "" else user["NickName"]
        temp = {}
        for key, value in sorted(self.udict_fin.items(), key=lambda x: x[1]):
            temp[key] = value
        self.udict_fin = temp
        self.udict_fin.pop(Sys.my_uid)
        self.udict_all = copy.deepcopy(self.udict_fin)

        self.__get_condition(content_list)
        for func in [self.__process_except, self.__process_only, self.__process_add]:
            func()
        if len(self.udict_fin) > 0:
            self.__send_target_users()
            return "TRUE"
        else:
            print(Broadcasting.warn_no_receiver)
            return "FALSE"

    def broadcasting_confirm(self, msg):
        uin = msg.Content
        if len(self.udict_fin) == 0:
            itchat.send(Broadcasting.warn_no_receiver, 'filehelper')
            return "FALSE"
        v_in = list(self.udict_fin.values())
        k_in = list(self.udict_fin.keys())
        if uin.lower() in ["y", "yes"]:
            self.__broadcasting_send()
            return "TRUE"
        elif uin.lower() in ["n", "no"]:
            itchat.send(Broadcasting.info_exit, 'filehelper')
            return "FALSE"
        uinput = list(filter(None, [e.strip() for e in uin.split("@")]))
        if len(uinput) == 0:
            if self.wrong_time < 2:
                itchat.send(Broadcasting.warn_wrong_input, 'filehelper')
                return "CONTINUE"
            else:
                itchat.send(Broadcasting.warn_exit, 'filehelper')
                return "FALSE"
        t_list = []
        for number in uinput:
            try:
                in_num = int(number)
                if in_num > len(v_in) or in_num < 1:
                    itchat.send(Broadcasting.warn_wrong_number % in_num, 'filehelper')
                else:
                    t_list.append(in_num)
            except ValueError:
                self.wrong_time += 1
                if self.wrong_time < 2:
                    itchat.send(Broadcasting.warn_wrong_input, 'filehelper')
                    return "CONTINUE"
                else:
                    itchat.send(Broadcasting.warn_exit, 'filehelper')
                    return "FALSE"
        uinput = t_list
        for number in uinput:
            itchat.send(Broadcasting.info_remove % self.udict_fin.pop(k_in[int(number) - 1]), 'filehelper')
            if len(self.udict_fin) == 0:
                itchat.send(Broadcasting.warn_no_receiver, 'filehelper')
                return "FALSE"
        self.__send_target_users()
        self.wrong_time = 0
        return "CONTINUE"

    def __broadcasting_send(self):
        for uid, uname in self.udict_fin.items():
            itchat.send(self.content, uid)

    def __send_target_users(self):
        message = ""
        v_in = list(self.udict_fin.values())
        counter = 1
        message += Broadcasting.prefix + "如下是你即将发送消息的联系人："
        for name in v_in:
            message += "\n%s   %s" % (counter, name)
            counter += 1
        message += "\n您可以直接输入号码删除被发送的联系人（多个号码请用@隔开），如果确认请回复Y，如果退出请回复N"
        itchat.send(message, 'filehelper')

    def __get_condition(self, content_list):
        for element in content_list:
            match = re.match("去除([:：])?", element)
            if match:
                self.except_list = list(filter(None, [e.strip() for e in element[match.end():].split("@", )]))
            match = re.match("仅包括([:：])?", element)
            if match:
                self.only_list = list(filter(None, [e.strip() for e in element[match.end():].split("@")]))
            match = re.match("加上([:：])?", element)
            if match:
                self.add_list = list(filter(None, [e.strip() for e in element[match.end():].split("@")]))

    def __process_except(self):
        temp = []
        if len(self.except_list) > 0:
            for e in self.except_list:
                for uid, uname in self.udict_fin.items():
                    if e in uname:
                        temp.append(uid)
            if len(temp) > 0:
                for uid in temp:
                    self.udict_fin.pop(uid)
            else:
                return
        else:
            return

    def __process_only(self):
        temp = []
        if len(self.only_list) > 0:
            for e in self.only_list:
                for uid, uname in self.udict_fin.items():
                    if e not in uname and uid not in temp:
                        temp.append(uid)
            if len(temp) > 0:
                for uid in temp:
                    self.udict_fin.pop(uid)
            else:
                return
        else:
            return

    def __process_add(self):
        temp = []
        if len(self.add_list) > 0:
            for e in self.add_list:
                for uid, uname in self.udict_all.items():
                    if e in uname:
                        temp.append(uid)
            if len(temp) > 0:
                for uid in temp:
                    self.udict_fin[uid] = self.udict_all[uid]
            else:
                return
        else:
            return
