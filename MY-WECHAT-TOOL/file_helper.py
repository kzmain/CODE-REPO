import itchat

from Function.AutoReply import AutoReply
from Function.Broadcasting import Broadcasting


# fh = file helper
from Function.Status import Status
from System.Error import Error


class file_helper:
    fh_obj = None
    fh_func = None

    fh_start_dict = {"群发": {"fhobj": Broadcasting, "fh_func": "broadcasting_prepare"},
                     "消除": {"fhobj": AutoReply, "fh_func": "clear_all_history_message"},
                     "状态": {"fhobj": Status, "fh_func": "change_status"}}
    fh_funct_dict = {"broadcasting_prepare": {"TRUE": "broadcasting_confirm", "CONTINUE": None, "FALSE": None},
                     "broadcasting_confirm": {"TRUE": None, "CONTINUE": "broadcasting_confirm", "FALSE": None}}

    @staticmethod
    def fh_start_new_task(task, argv):
        try:
            file_helper.fh_obj = file_helper.fh_start_dict[task]["fhobj"]()
            file_helper.fh_func = getattr(file_helper.fh_obj, file_helper.fh_start_dict[task]["fh_func"])
            file_helper.fh_continue_previous_task(argv)
        except (Error, KeyError):
            itchat.send("指令输入错误!", 'filehelper')

    @staticmethod
    def fh_continue_previous_task(argv):
        try:
            result = file_helper.fh_func(argv)
            next_mn = file_helper.fh_funct_dict[file_helper.fh_func.__name__][result]
        except (Error, KeyError):
            next_mn = None

        if next_mn is not None:
            file_helper.fh_func = getattr(file_helper.fh_obj, next_mn)
        else:
            file_helper.fh_obj = None
            file_helper.fh_func = None

    @staticmethod
    def fh_check_task(msg):
        content_list = msg.Content.split("|")
        content_list.reverse()
        return content_list


