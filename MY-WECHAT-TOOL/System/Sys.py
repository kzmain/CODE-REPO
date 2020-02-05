class Sys:
    my_uid = None

    @staticmethod
    def choose_console_color():
        while True:
            try:
                screen = int(input("你的控制台是什么颜色呢？黑色请输入1，白色请输入2\n"))
                if screen in [1, 2]:
                    if screen == 1:
                        qr_in = 2
                    else:
                        qr_in = -2
                    return qr_in
            except TypeError:
                print("输入错误")
