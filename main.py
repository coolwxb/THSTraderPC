import concurrent
import os
import sys
from concurrent.futures.thread import ThreadPoolExecutor

from datetime import datetime, time
import time as ttime

import threading

import alert

import rule
import ticket
import ths

import jiaogedan as jg
import mss
import msg

conceptMap = {}  # 概念
# 近期热门行业
recentIndustryConceptList = []
current_stocks = {}

# 创建一个共享的锁
shared_lock = threading.Lock()

mssObj = mss.Mss(shared_lock=shared_lock)
alertObj = alert.Alert(shared_lock=shared_lock)
thsObj = ths.Ths(shared_lock=shared_lock)


# 解析新增内容的方法，获取第一列作为股票代码
def parse_content(content):
    columns = content.split(' ')
    if len(columns) >= 2:
        stock_code = columns[0]
        stock_name = columns[1]
        return stock_code, stock_name
    return "0", content


def is_time_to_sell(hour, minute):
    current_time = datetime.now().time()
    target_time = time(hour, minute)  # 目标时间下午2点50分
    if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
        return True
    else:
        return False

AM_TRADING_START = time(9, 25, 0)
AM_TRADING_END = time(11, 30, 0)
PM_TRADING_START = time(13, 0, 0)
PM_TRADING_END = time(15, 0, 0)
# 开盘时间
def is_deal_time():
    now = datetime.now().time()
    if AM_TRADING_START <= now <= AM_TRADING_END or PM_TRADING_START <= now <= PM_TRADING_END:
        return True
    else:
        return False
    # return True




def is_shoupan():
    # 假设交易时间从 9:30 到 16:00
    now = datetime.now().time()
    PM_TRADING_END = time(14, 59, 0)
    if PM_TRADING_END <= now:
        return True
    else:
        return False
    # return False


# 监听文件变化的方法
def watch_file(path='预警.txt', share_lock=shared_lock):
        if not os.path.exists(path):
            # 文件不存在，创建文件jjjzxyj
            with open(path, 'w', encoding="utf-8") as file:
                pass
    # while True:
        try:
            share_lock.acquire()
            print("watch_file======获取锁")
            if is_shoupan():
                j = jg.Jiaogedan()
                j.clear_all()
                with open('预警.txt', 'w', encoding="utf-8") as f:
                    f.write('')
                with open('chicang.txt', 'w', encoding="utf-8") as f:
                    f.write('')
                sys.exit()

            elif is_deal_time():
                mssObj.call_tdx_alert()
                with open(path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
                    print(lines)
                for line_s in lines:
                    # 使用 rstrip 方法去除末尾的换行符 \n
                    line = line_s.rstrip('\n')
                    if line == "":
                        continue
                    if line in current_stocks:
                        continue
                    else:
                        current_stocks[line] = line
                        if line == "":
                            continue
                        else:
                            parsed_code, stock_name = parse_content(line)
                            print(parsed_code, stock_name)
                            print("===")
                            if len(parsed_code) != 6:
                                print(f"{parsed_code} {stock_name} code 错误")
                                with open('预警.txt', 'w', encoding="utf-8") as f:
                                    f.write('')
                                continue
                            else:
                                if rule.fitTicket(parsed_code,stock_name):
                                    # if True:
                                    # 判断是否是近期热点
                                    flag = True
                                    if not flag:
                                        print(f"f{parsed_code}  {stock_name}不是近期热点")
                                    else:
                                        mssObj.click_soft()
                                        ttime.sleep(1)
                                        purple_up, purple_price, gray_price_up, gray_price_down = alertObj.purple_price(
                                            parsed_code)
                                        if purple_price == 0 and gray_price_up == 0 and gray_price_down == 0:
                                            # 超过最大尝试次数仍未获取到非零的price1
                                            # 在这里处理相应逻辑
                                            print(f"获取{parsed_code}  {stock_name}的紫色线价格失败")
                                            msg.dingding.send_msg(f"获取{parsed_code} {stock_name}的紫色线价格失败")
                                        elif gray_price_up >= purple_up or gray_price_up >= purple_price:
                                            print(f"{parsed_code}的灰色线在紫色线上方，不符合强势条件")
                                            msg.dingding.send_msg(
                                                f"{parsed_code}  {stock_name} 的灰色线在紫色线上方，不符合强势条件")
                                        else:
                                            current = ticket.TicketInfo().get_realtime_ticket_info(parsed_code)
                                            print(f"当前{parsed_code}  {stock_name} 价格为{current}")
                                            # # 调查活跃度
                                            # if current==0:
                                            #     continue
                                            # else:
                                            #     thsObj.buy(parsed_code, current)
                                            #     msg.dingding.send_msg(
                                            #         f"当前{parsed_code}  {stock_name}买入价格为{current}")
                                            if current == 0:
                                                continue
                                            if current <= gray_price_down and gray_price_down != 0:
                                                thsObj.buy(parsed_code, current)
                                                msg.dingding.send_msg(
                                                    f"当前{parsed_code}  {stock_name} 买入价格为{current}")
                                            elif current < purple_price and current > gray_price_up and purple_price != 0 and gray_price_up != 0:
                                                thsObj.buy(parsed_code, gray_price_up)
                                                msg.dingding.send_msg(
                                                    f"当前{parsed_code}  {stock_name}买入价格为{gray_price_up}")
                                            elif current < gray_price_up and current > gray_price_down and gray_price_up != 0:
                                                thsObj.buy(parsed_code, current)
                                                msg.dingding.send_msg(
                                                    f"当前{parsed_code}  {stock_name}买入价格为{current}")
                                            elif current < gray_price_down and gray_price_up != 0:
                                                thsObj.buy(parsed_code, current)
                                                msg.dingding.send_msg(
                                                    f"当前{parsed_code}  {stock_name}买入价格为{current}")
                                            else:
                                                thsObj.buy(parsed_code, purple_price)
                                                msg.dingding.send_msg(
                                                    f"当前{parsed_code}  {stock_name}买入价格为{purple_price}")
            ttime.sleep(5)
        except Exception as e:
            print("watch_file 报错")
            print(e)
            raise RuntimeError('watch_file Error')
        finally:
            share_lock.release()
            print("watch_file======释放锁")


# 启动并管理任务
def submit_task_with_retry(executor, task_func, retries=5):
    attempt = 0
    while attempt < retries:
        try:
            # 提交任务到线程池
            future = executor.submit(task_func)
            return future.result()  # 获取任务结果，如果任务抛出异常会在这里捕获
        except Exception as e:
            attempt += 1
            print(f"任务失败，重试 {attempt}/{retries} 次，错误: {e}")
            if attempt >= retries:
                print("达到最大重试次数，任务失败")
                return None  # 达到最大重试次数，返回失败
            ttime.sleep(2)  # 等待一段时间再重试


if __name__ == '__main__':

    with ThreadPoolExecutor(max_workers=3) as executor:
        mssObj.click_trade_soft()
        thsObj.open_position()
        # result_futures = [executor.submit(watch_file), executor.submit(thsObj.sell_strategy)]
        # for future in concurrent.futures.as_completed(result_futures):
        while True:
            try:

                watch_file()
                thsObj.sell_strategy()

            except Exception as e:  # 捕获子线程中的异常
                print('>>> main ThreadPoolExecutor, e: ', e.args)  # 成功捕获异常
                # Decide which task to re-submit based on the exception or failure
                # if isinstance(e, ValueError):  # Assuming ValueError comes from task 1
                #     # Re-submit task 1 after failure
                #     result_futures.append(executor.submit(thsObj.sell_strategy))
                #     msg.dingding.send_msg(f"自动重启售卖任务\r\n{e.args}")
                # else:
                #     # Re-submit task 2 or handle other types of exceptions as needed
                #     result_futures.append(executor.submit(watch_file()))
                #     msg.dingding.send_msg(f"自动重启监听买入任务\r\n{e.args}")

