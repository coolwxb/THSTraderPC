import json

import requests


webhook = "https://oapi.dingtalk.com/robot/send?access_token=fad0dff0a7f553c5c1c8b9db56dc85f19392e0d72b9d8629627e748a123db6a4"
header = {"Content-Type": "application/json; charset=utf-8"}




def send_msg(content, webhook=webhook):
    data = {
        "msgtype": "text",
        "text": {
            "content": "alert:" + content
        }
    }
    r = requests.post(f'{webhook}', data=json.dumps(data), headers=header)
    print(r)


send_msg("你好好")
