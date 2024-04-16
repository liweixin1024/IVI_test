import time
import hmac
import base64
import urllib.parse
import json
import urllib.request
import requests


class DingTalkBot:

    def send_dd_message(self, web_url, message, keyword, at_all=False):
        """
        发送钉钉群消息,在钉钉机器人上设置关键词，message需要包含这个这个关键词，大小写不敏感
        :param web_url: robot webpage url
        :param message: send info
        :param keyword: key words
        :param at_all: yes or no @ anybody
        :return:
        """
        if keyword.lower() not in message.lower():
            raise Exception("ERROR:message needs to include the keyword")
        headers = {"Content-Type": "application/json;charset=utf-8"}
        data = {
            "msgtype": "text",
            "text": {
                "content": message
            },
            "at": {
                "isAtAll": at_all
            }
        }
        response = requests.post(web_url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            raise Exception("[WARNING]:send ding ding message failed!")

    def send_dbtest_info(self, db_ver: str, res: bool):
        # 给钉钉上项目群发送消息
        key_word = 'DB版本点检'
        dd_url = "https://oapi.dingtalk.com/robot/send?access_token=30e018298cc1f7deea1dbaefe84eefd64ee83c4455f785c42a0d17da9a8c5422"
        info = "[DB版本点检]\n\n" + \
               "版本信息：{}\n".format(db_ver) + \
               'DB版本点检结果：{}\n'.format(res)
        try:
            self.send_dd_message(dd_url, info, key_word, at_all=True)
            # retry_run(3, 10, send_dd_message, dd_url, info, self.c_env.SOC, at_all=True)
        except Exception as dd_err:
            print(dd_err)


if __name__ == '__main__':
    dt = DingTalkBot()
    dt.send_dbtest_info(db_ver="GACNE_A19_AVNT_ST_240307_1631D_D", res=True)
