import os
import sched
import time
import datetime
import msg
import numpy as np
import requests
from PIL import ImageGrab
from easyocr import easyocr

import tdx_module
import ths
import pandas as pd
import re

import ticket
import jiaogedan as jg

conceptMap = {}  # 概念
# 近期热门行业
recentIndustryConceptList = []


# 判断时间
def is_time_to_sell(hour, minute):
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour, minute)  # 目标时间下午2点50分
    if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
        return True
    else:
        return False


# 定义监测屏幕范围变量
screen_rect = (1420, 1, 1420 + 181, 1 + 24)
# 先前的屏幕截屏
previous_screen = None

reader = easyocr.Reader(['ch_sim', 'en'])

# 定义已经预警过的code，用来识别是否重复预警
alert_codes = []


# 监控文件变化的方法
def watch_screen():
    while True:
        # 到时间执行
        if is_time_to_sell(14, 52):
            # 执行卖出操作
            print("当前时间是下午2点50分，执行卖出操作")
            ths.Ths().sell()
            # 清空购买记录
            jg.Jiaogedan().clear_all()
            return
        elif is_time_to_sell(9, 25):
            # 执行开盘卖出策略
            print("当前时间是下午9点25分，执行卖出操作")
            ths.Ths().open_sell()
        elif is_time_to_sell(10, 55):
            # 执行开盘卖出策略
            print("当前时间是上午10点55分，取消所有买入操作，重新挂出卖单")
            ths.Ths().cancel_all_entrusts()
            ths.Ths().open_sell()
        # 每次截屏前要返回通达信主界面，否则会截取到其他界面

        # 监控屏幕变化
        img = ImageGrab.grab(bbox=screen_rect)
        screen = np.array(img)
        if previous_screen is None:
            previous_screen = screen
        if not np.array_equal(screen, previous_screen):
            # 屏幕内容不同
            infos = reader.readtext(screen)
            if len(infos) > 0:
                # 遍历元组数组，打印数据
                for info in infos:
                    # 判断code[1] 是否为6位数字
                    if info[1].isdigit() and len(info[1]) == 6:
                        parsed_code = info[1]
                        # 判断 parsed_code 是否遍历过
                        if parsed_code in alert_codes:
                            continue
                        else:
                            alert_codes.append(parsed_code)
                        purple_price, gray_up_price, gray_down_price = tdx_module.Alert().purple_price(parsed_code)
                        if purple_price == 0 and gray_up_price == 0 and gray_down_price == 0:
                            print(f"获取{parsed_code}的紫色线价格失败")
                            msg.dingding.send_msg(f"获取{parsed_code}的紫色线价格失败")
                        else:
                            # 获取当前价格
                            t = ths.Ths()
                            current = ticket.TicketInfo().get_realtime_ticket_info(parsed_code)
                            # 对比价格执行买入逻辑
                            if current <= gray_down_price and gray_down_price != 0:
                                print(f"{parsed_code} 跌破灰色下价格，不买入")
                            elif current < purple_price and current > gray_up_price and purple_price != 0 and gray_up_price != 0:
                                t.buy(parsed_code, gray_up_price)
                            elif current < gray_up_price and gray_up_price != 0:
                                t.buy(parsed_code, current)
                            else:
                                t.buy(parsed_code, purple_price)
                    else:
                        # 解析错误code 发送消息
                        msg.dingding.send_msg(f"监控屏幕，出现错误code：{info[1]}")


if __name__ == '__main__':
    try:
        watch_screen()
    except Exception:
        msg.dingding.send_msg("股票交易报错停止了")
