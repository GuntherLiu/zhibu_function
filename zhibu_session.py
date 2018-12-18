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
        logger.logger(body, url)
        sleep(3)
        res = self.session.post(url,data=body, headers=self.headers)
        return res

    def do_get(self, url):
        logger.logger(url, 'the get method')
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
                "password": '363636',
                "captcha_code": int(auth_code),
                "captcha_token": captcha_token
            }
            res = self.do_post(login_url, post_data)
            logger.logger(res.content, 'the login post response')

            if not self.is_login() and ind < 50:
                ind += 1
                print '%d%s%s' % (ind, ',the auth code is wrong: ', auth_code)
            else:
                print 'login success'
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
        auth_code = raw_input("input auth ode: ")

        return captcha_token, auth_code

    def is_login(self):
        logger.logger('judge weather it is login')
        is_login_url = 'https://capi.dangjianwang.com/official/ucenter/login/webuserinfo'
        content = self.do_get(is_login_url).json()
        if content['code'] != 200 and content['msg'] != 'ok':
            return False
        else:
            return True
