#encoding=utf-8
import logger
import requests
import re
from time import sleep


class ZhibuSession:
    def __init__(self):
        logger.logger('create a new session')
        self.session = requests.session()
        self.headers = {
            'Appid': 'd48bc5e9ddaeff70',
            'Origin': "https://www.zhibugongzuo.com",
            'Referer': "https://www.zhibugongzuo.com/login",
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        }

    def do_post(self, url, body):
        sleep(3)
        res = self.session.post(url, data=body, headers=self.headers)
        return res

    def do_get(self, url):
        sleep(3)
        res = self.session.get(url, headers=self.headers)
        return res

    def do_login(self):
        logger.logger('the login function')
        login_url = "https://capi.dangjianwang.com/official/ucenter/login/index"
        ind = 0
        while True:
            captcha_token, auth_code = self.get_token()
            if re.search(r'\D', auth_code) or auth_code == '':
                continue
            post_data = {
                "username": 'qianliying',
                "password": 'ql363636',
                "captcha_code": int(auth_code),
                "captcha_token": captcha_token
            }
            res = self.do_post(login_url, post_data)
            # logger.logger(res.content, 'the login post response')

            if not self.is_login() and ind < 50:
                ind += 1
                logger.logger('%d%s%s' % (ind, ',the auth code is wrong: ', auth_code))
            else:
                logger.logger('login success')
                break
        return True

    def get_token(self):
        logger.logger('get token capcha')
        captcha_url = "https://capi.dangjianwang.com/official/ucenter/login/preCaptcha"
        content = self.do_get(captcha_url).json()
        i_captcha_url = content['data']['captcha_url']
        captcha_token = content['data']['captcha_token']
        t = self.do_get(i_captcha_url)
        with open("captcha.png", "wb") as f:
            f.write(t.content)
            f.close()
        # auth_code = input("input auth ode: ")
        auth_code = self.verify_code()
        return captcha_token, auth_code

    def verify_code(self):
        sleep(5)
        u2 = "http://api.95man.com:8888/api/Http/Recog?Taken=9hnx0XNLyB5uY3N09Lq6XHNcMWx4&imgtype=2&len=4"
        files = {
            'file': open('captcha.png', 'rb')
        }
        res = requests.post(url=u2, files=files)
        t = res.text
        logger.logger('%s%s' % ('get the code: ', t))
        ts = t.split('|')
        code = ts[1]
        return code

    def is_login(self):
        logger.logger('judge weather it is login')
        is_login_url = 'https://capi.dangjianwang.com/official/ucenter/login/webuserinfo'
        content = self.do_get(is_login_url).json()
        if content['code'] != 200 and content['msg'] != 'ok':
            return False
        else:
            return True

    def test(self):
        u1 = "http://api.95man.com:8888/api/Http/UserTaken?user=KingZhao&pwd=296732774&isref=0"
        u2 = "http://api.95man.com:8888/api/Http/Recog?Taken=9hnx0XNLyB5uY3N09Lq6XHNcMWx4&imgtype=2&len=4"
        # res = self.do_get(u1)
        # logger.logger(res.text)

        files = {
            'file': open('captcha.png', 'rb')
        }
        # res = requests.post(url=u2, files=files)
        t = '3927421|1996|0'
        ts = t.split('|')
        logger.logger(ts[1])


if __name__ == '__main__':
    testSession = ZhibuSession()
    testSession.test()



