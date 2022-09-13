import re
import time

import requests
from bs4 import BeautifulSoup
import common.Oubk as oubk
import solver.solver as solver
import json
from oubk.authentication.auth import get_oubk_auth_instance


class DailySudoku:
    url = None
    # 数独
    pz = None
    # 日期ID
    daily_id = None
    # 显示日期编号
    show_days = None
    # 难度等级
    pn = None
    # 数独ID
    pz_id = None
    # 解题步骤
    active_source = "4s9$1|0#"
    # 解题用时
    time_used = 0
    # 用户ID
    user_id = None
    # 答案
    answer = ""
    # 错误信息
    err_msg = []
    # 认证模块
    auth = get_oubk_auth_instance()

    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    def calc_sudoku(self) -> None:
        """
        数独解题
        生成答案
        生成解题步骤
        :return:
        """
        print("开始解题")

    def get_sudoku(self):
        response = requests.get(url=self.url)
        html_doc = response.content.decode()
        # print(html_doc)
        soup = BeautifulSoup(html_doc, 'html.parser')
        # 获取答案
        self.answer = soup.find(id='hid_aw')['value']
        # "daily_id":13136,"show_days":18679,"pn":1,"pz_id":1768
        # 获取 daily_id
        daily_id_regx = r"daily_id\":(\d+)"
        self.daily_id = re.findall(daily_id_regx, html_doc)[0]
        # 获取 show_days
        show_days_regx = r"show_days\":(\d+)"
        self.show_days = re.findall(show_days_regx, html_doc)[0]
        # 获取 pn
        pn_regx = r"\"pn\":(\d+)"
        self.pn = re.findall(pn_regx, html_doc)[0]
        # 获取 pz_id
        pz_id_regx = r"\"pz_id\":(\d+)"
        self.pz_id = re.findall(pz_id_regx, html_doc)[0]

        self.time_used = 1
        self.user_id = self.auth.get_user_id()

    def save(self) -> bool:
        """
        保存成绩
        :return:
        """
        # 获取数独信息
        self.get_sudoku()
        if self.daily_id is None or self.daily_id == "":
            self.err_msg.append("daily_id 不能为空")
            return False
        if self.show_days is None or self.show_days == "":
            self.err_msg.append("show_days 不能为空")
            return False
        if self.pn is None or self.pn == "":
            self.err_msg.append("pn 不能为空")
            return False
        if self.pz_id is None or self.pz_id == "":
            self.err_msg.append("pz_id 不能为空")
            return False
        if self.active_source is None or self.active_source == "":
            self.err_msg.append("active_source 不能为空")
            return False
        if self.time_used is None or self.time_used == "":
            self.err_msg.append("time_used 不能为空")
            return False
        if self.user_id is None or self.user_id == "":
            self.err_msg.append("user_id 不能为空")
            return False
        if self.answer is None or self.answer == "":
            self.err_msg.append("answer 不能为空")
            return False
        return self.do_save_post()

    def do_save_post(self) -> bool:
        # 构造data
        data = {
            "daily_id": self.daily_id,
            "show_days": self.show_days,
            "pn": self.pn,
            "pz_id": self.pz_id,
            "active_source": self.active_source,
            "time_used": self.time_used,
            "user_id": self.user_id,
            "answer": self.answer
        }
        save_url = oubk.save_url
        headers = self.auth.get_auth_header(self.url)
        response = requests.post(url=save_url, data=data, headers=headers)
        json_res = response.content.decode()
        content = json.loads(json_res)
        if content['code'] != 8005:
            self.err_msg.append(content['message'])
            return False
        return True


if __name__ == '__main__':
    n = 18409
    while n > 0:
        for pn in range(1, 6):
            daily_sudoku_url = "http://p.oubk.com/DailySudoku/%d/%d" % (n, pn)
            daily_sudoku = DailySudoku(daily_sudoku_url)
            save_res = daily_sudoku.save()
            if not save_res:
                print("答题失败:%s,错误原因:%s" % (daily_sudoku_url, str(daily_sudoku.err_msg)))
                daily_sudoku.err_msg.clear()
            else:
                print("答题完成:%s,休息1s..." % daily_sudoku_url)
            time.sleep(1)
        n -= 1
