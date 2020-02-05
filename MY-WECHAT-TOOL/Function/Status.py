import itchat

from Function.AutoReply import AutoReply
from System.Error import Error


class Status:
    status_dict = {"OFFLINE": "离线",
                   "ONLINE": "在线"}
    current_status = "离线"

    @staticmethod
    def change_status(status_list):
        try:
            change_status = status_list[0]
        except (Exception, IndexError):
            raise Error
        if change_status != Status.current_status:
            if change_status == "在线":
                AutoReply.stop_auto_reply()
                Status.current_status = "在线"
            elif change_status == "离线":
                AutoReply.start_auto_reply()
                Status.current_status = "离线"
        itchat.send("状态更新为" + Status.current_status, 'filehelper')
