import requests


# 向微信公众号 方糖  发送消息
def send_msg_to_WX(title, content):
    # 钉钉机器人的Webhook地址，需要替换为实际地址
    webhook = "https://sctapi.ftqq.com/SCT231940TOqVp5vSDXB0FR6gsLJ1OKqDW.send?title=" + title + "&desp=" + content
    requests.get(url=webhook)
