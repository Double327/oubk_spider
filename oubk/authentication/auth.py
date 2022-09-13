import requests


class OubkAuth:
    oubk_cookie = ""
    _xsrf = ""
    user_id = "188254"
    nickname = ""
    username = ""
    password = ""
    login_url = "http://p.oubk.com/login"

    def __init__(self, username, password) -> None:
        super().__init__()
        self.username = username
        self.password = password

    def login(self):
        print("登录中---")
        # TODO: xsrf 可能需要动态生成一下
        # 表单数据
        data = {
            '_xsrf': '2|bc0a8aac|9f26473f8f192ca5c92320097f2f48b8|1662986726',
            'login_name': self.username,
            'password': self.password
        }
        response = self.do_login(url=self.login_url, data=data)
        # TODO: 根据 content 里的内容判断一下是否登录成功了
        self.oubk_cookie = response.cookies['oubk']
        # self._xsrf = response.cookies['_xsrf']
        print("登录结束---")

    def do_login(self, url, data):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://p.oubk.com/login'
        }
        # 'Cookie': '_xsrf=2|f74479d9|d468b44ac457dfd0826dd37c3461bbcd|1662986726; ClientTzo=8; Hm_lvt_8769d790727a6d26a7aac27214c5c38d=1662983410; Hm_lpvt_8769d790727a6d26a7aac27214c5c38d=1662987561; oubk="2|1:0|10:1662987569|4:oubk|144:eyJsYW5nIjogInpoX0NOIiwgIm5hbWUiOiAiXHU2ZDZlXHU3MGI5XHU2NTcwIiwgImlwIjogIjEyMS4yMjUuMTE1Ljg4IiwgInRzIjogMCwgInRiIjogMjg4MDAsICJpZCI6IDE4ODI1NH0=|1913a323bf07029087e80b0310391d0732c2109927def702c7387c67b85afa55"
        return requests.post(url=url, data=data, headers=headers)

    def test(self):
        print("hello")

    def my_info(self):
        url = "http://p.oubk.com/浮点数"
        cookie_str = self.get_login_cookie()
        return self.do_get(url, cookie_str)

    def do_get(self, url, cookie: str):
        print(cookie)
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            # 'Referer': 'http://p.oubk.com/my',
            'Referer': 'http://p.oubk.com/%C3%A6%C2%B5%C2%AE%C3%A7%C2%82%C2%B9%C3%A6%C2%95%C2%B0',
            'Postman-Token': 'eaee26d2-d189-4085-b728-f5833e5e162a',
            'Host': 'p.oubk.com',
            # 'cookie': 'ClientTzo=8; Hm_lvt_8769d790727a6d26a7aac27214c5c38d=1662988534; Hm_lpvt_8769d790727a6d26a7aac27214c5c38d=1662988981; _xsrf=2|413f6516|b8fa68f08d6ce2b883f81c9d6aef4c48|1662988711; Hm_lvt_3b7c7d63910b4a54c54af1ff6698dd58=1662982136,1662988588; Hm_lpvt_3b7c7d63910b4a54c54af1ff6698dd58=1662988745; oubk="2|1:0|10:1662989816|4:oubk|144:eyJsYW5nIjogInpoX0NOIiwgIm5hbWUiOiAiXHU2ZDZlXHU3MGI5XHU2NTcwIiwgImlwIjogIjEyMS4yMjUuMTE1Ljg4IiwgInRzIjogMCwgInRiIjogMjg4MDAsICJpZCI6IDE4ODI1NH0=|955c2c20fa58efdf1353892853dac44200ecae4e2571fd037a8440e69ccfa630"; __gads=ID=de5cd29ee180c08b-221981606bd600d1:T=1662988981:RT=1662988981:S=ALNI_MYKFUUNVoM42aoPj3Jy87Kgt-u66A; __gpi=UID=0000085b03dc6a13:T=1662988981:RT=1662988981:S=ALNI_MZieVqT_aVLbhfpSrSbsVVpro8_Rg'
            'cookie': cookie
        }
        print(header)
        response = requests.get(url, headers=header)
        return response

    def get_login_cookie(self) -> str:
        # 验证一下有没有登录
        if not self.is_authed():
            self.login()
        cookie = """oubk=%s; Path=/; Domain=oubk.com;""" % self.oubk_cookie
        return cookie

    def is_authed(self) -> bool:
        if self.oubk_cookie is None or self.oubk_cookie == "":
            return False
        return True

    def get_auth_header(self, referer):
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': referer,
            'Host': 'p.oubk.com',
            'cookie': self.get_login_cookie()
        }
        return header

    def get_user_id(self) -> str:
        return self.user_id


def get_oubk_auth_instance() -> OubkAuth:
    return OubkAuth('123123936@qq.com', '123456789')


if __name__ == '__main__':
    auth = OubkAuth('123123936@qq.com', '123456789')
    print(auth.my_info().content.decode())
    print(auth.my_info().content.decode().find("我的最新动态") != -1)
