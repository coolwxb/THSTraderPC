import os
import sched
import time
from datetime import datetime

import alert
import ths
import pandas as pd
import re

import ticket

conceptMap = {} # 概念
# 近期热门行业
recentIndustryConceptList = []


# 解析新增内容的方法，获取第一列作为股票代码
def parse_content(content):
    columns = content.split('\t')
    stock_code = columns[0]
    return stock_code

# 监听文件变化的方法
def watch_file(path):
    file = open(path)
    while True:
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
            flag = False
            for industry in recentIndustryConceptList:
                if parsed_code in conceptMap:
                    if industry in conceptMap[parsed_code]['行业']:
                        flag = True
                        break
            if not flag:
                for concept in recentIndustryConceptList:
                    if parsed_code in conceptMap:
                        if concept in conceptMap[parsed_code]['概念']:
                            flag = True
                            break
            if not flag:
                print(f"{parsed_code}不是近期热门异动板块概念")
                continue
            else:
                print(f"{parsed_code}是近期热门异动板块概念")

                max_attempts = 3
                attempt = 1
                price1 = 0

                while attempt <= max_attempts:
                    price1, price2,price3  = alert.Alert().purple_price(parsed_code)
                    if price1 != 0 and re.match(r"\d+\.\d{2}$", str(price1)):
                        break
                    attempt += 1

                if price1 == 0:
                    # 超过最大尝试次数仍未获取到非零的price1
                    # 在这里处理相应逻辑
                    print(f"获取{parsed_code}的紫色线价格失败")
                else:
                    # 处理获取到的price1
                    # 判断当前价格是否小于紫色线价格
                    t = ths.Ths()
                    current = ticket.TicketInfo().get_realtime_ticket_info(parsed_code)
                    if current <= price3:
                        print(f"{parsed_code} 跌破灰色下价格，不买入")
                    elif current < price1 and current > price2:
                        t.buy(parsed_code, price2)
                    elif current < price2:
                        t.buy(parsed_code, current)
                    else:
                        t.buy(parsed_code,price1)





if __name__ == '__main__':
    # 读取概念信息
    df = pd.read_excel('股票行业、板块信息.xlsx',converters={'代码': str})
    conceptMap = df.set_index('代码').T.to_dict()
    # 将热点板块信息读取到内存
    f = open("recent_industry_concept.txt",encoding='utf-8')
    recentIndustryConceptList = f.read().splitlines()
    f.close()

    # 启动文件监听
    watch_file('预警.txt')

    # 每日下午三点半执行方法

