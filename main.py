import os
import sched
import time
import datetime

import requests

import alert
import mss
import ths
import pandas as pd
import re

import ticket
import jiaogedan as jg
import mss

conceptMap = {} # 概念
# 近期热门行业
recentIndustryConceptList = []


# 解析新增内容的方法，获取第一列作为股票代码
def parse_content(content):
    columns = content.split(' ')
    stock_code = columns[0]
    return stock_code

# 判断时间
def is_time_to_sell(hour,minute):
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour, minute)  # 目标时间下午2点50分
    if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
        return True
    else:
        return False

# 向钉钉发送消息
def send_msg_to_dingtalk(title,content):
    # 钉钉机器人的Webhook地址，需要替换为实际地址
    webhook = "https://sctapi.ftqq.com/SCT231940TOqVp5vSDXB0FR6gsLJ1OKqDW.send?title="+title+"&desp="+content
    requests.get(url=webhook)
# 监听文件变化的方法
def watch_file(path):
    if not os.path.exists(path):
        # 文件不存在，创建文件
        with open(path, 'w',encoding="utf-8") as file:
            pass
    file = open(path)
    while True:

        # 示例使用
        if is_time_to_sell(14,52):
            # 执行卖出操作
            print("当前时间是下午2点50分，执行卖出操作")
            ths.Ths().sell()
            # 清空购买记录
            jg.Jiaogedan().clear_all()
            return
        elif is_time_to_sell(9,25):
            # 执行开盘卖出策略
            print("当前时间是下午9点25分，执行卖出操作")
            ths.Ths().open_sell()
        elif is_time_to_sell(10,55):
            # 执行开盘卖出策略
            print("当前时间是上午10点55分，取消所有买入操作，重新挂出卖单")
            ths.Ths().quxiao()
            ths.Ths().open_sell()
            return
        # 将代码复制到预警里
        # mss.call_tdx_alert()

        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(5)
            file.seek(where)
            mss.call_tdx_alert()
        else:
            print(line, end='')
            parsed_code = parse_content(line)
            if len(parsed_code)!=6:
                print(f"{parsed_code} code 错误")
                continue
            else:
                print(parsed_code+"-----")
                print(f"{parsed_code}是近期热门异动板块概念")
                purple_price, gray_price_up,gray_price_down  = alert.Alert().purple_price(parsed_code)
                if purple_price == 0 and gray_price_up==0 and gray_price_down==0:
                    # 超过最大尝试次数仍未获取到非零的price1
                    # 在这里处理相应逻辑
                    print(f"获取{parsed_code}的紫色线价格失败")
                else:
                    pass
                    # 处理获取到的price1
                    # 判断当前价格是否小于紫色线价格
                    t = ths.Ths()
                    current = ticket.TicketInfo().get_stock_individual_info_em(parsed_code)
                    if current <= gray_price_down and gray_price_down!=0:
                        t.buy(parsed_code, current)
                    elif current < purple_price and current > gray_price_up and purple_price!=0 and gray_price_up!=0:
                        t.buy(parsed_code, gray_price_up)
                    elif current < gray_price_up and gray_price_up!=0:
                        t.buy(parsed_code, current)
                    else:
                        t.buy(parsed_code,purple_price)





if __name__ == '__main__':
    # 读取概念信息
    # df = pd.read_excel('股票行业、板块信息.xlsx',converters={'代码': str})
    # conceptMap = df.set_index('代码').T.to_dict()
    # 将热点板块信息读取到内存
    # f = open("recent_industry_concept.txt",encoding='utf-8')
    # recentIndustryConceptList = f.read().splitlines()
    # f.close()

    try:
        watch_file('预警.txt')
    except Exception:
        send_msg_to_dingtalk("股票交易自动停止了", "出错了")
        # send_msg_to_dingtalk("监听报错退出了")

    # 每日下午三点半执行方法

