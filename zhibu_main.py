import save_util
import func_do


class Main:
    def __init__(self):
        print 'the main class'

    def judge(self):
        print 'judge is login or not'
        self.zhibu_session = save_util.do_read()
        if self.zhibu_session.is_login():
            print 'the zhibu session is login'
            func_do.test()
        else:
            print 'the zhibu session is not login'
            save_util.test()
            self.judge()


def test():
    main = Main()
    main.judge()


if __name__ == '__main__':
    test()
