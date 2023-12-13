import os
import sched
import time
import datetime

import requests

import alert
import ths
import pandas as pd
import re

import ticket
import jiaogedan as jg

conceptMap = {} # 概念
# 近期热门行业
recentIndustryConceptList = []


# 解析新增内容的方法，获取第一列作为股票代码
def parse_content(content):
    columns = content.split('\t')
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
            print("当前时间是下午10点55分，取消所有操作")
            ths.Ths().quxiao()

        where = file.tell()
        line = file.readline()
        if not line:
            time.sleep(1)
            file.seek(where)
        else:
            print(line, end='')
            parsed_code = parse_content(line)

            # 根据优化策略判断是否买入股票
            # 1、是近期7天热门异动板块概念
            flag = True
            # for industry in recentIndustryConceptList:
            #     if parsed_code in conceptMap:
            #         if industry in conceptMap[parsed_code]['行业']:
            #             flag = True
            #             break
            # if not flag:
            #     for concept in recentIndustryConceptList:
            #         if parsed_code in conceptMap:
            #             if concept in conceptMap[parsed_code]['概念']:
            #                 flag = True
            #                 break
            if not flag:
                print(f"{parsed_code}不是近期热门异动板块概念")
                continue
            else:
                # print(f"{parsed_code}是近期热门异动板块概念")
                price1, price2,price3  = alert.Alert().purple_price(parsed_code)
                if price1 == 0 and price2==0 and price3==0:
                    # 超过最大尝试次数仍未获取到非零的price1
                    # 在这里处理相应逻辑
                    print(f"获取{parsed_code}的紫色线价格失败")
                else:
                    # 处理获取到的price1
                    # 判断当前价格是否小于紫色线价格
                    t = ths.Ths()
                    current = ticket.TicketInfo().get_realtime_ticket_info(parsed_code)
                    if current <= price3 and price3!=0:
                        print(f"{parsed_code} 跌破灰色下价格，不买入")
                    elif current < price1 and current > price2 and price1!=0 and price2!=0:
                        t.buy(parsed_code, price2)
                    elif current < price2 and price2!=0:
                        t.buy(parsed_code, current)
                    else:
                        t.buy(parsed_code,price1)





if __name__ == '__main__':
    # 读取概念信息
    df = pd.read_excel('股票行业、板块信息.xlsx',converters={'代码': str})
    conceptMap = df.set_index('代码').T.to_dict()
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

