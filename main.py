import os
import datetime
import threading

import alert
import rule
import ths
import time
import ticket
import jiaogedan as jg
import mss

conceptMap = {}  # 概念
# 近期热门行业
recentIndustryConceptList = []

# 创建一个共享的锁
shared_lock = threading.Lock()

mssObj = mss.Mss(shared_lock=shared_lock)
alertObj = alert.Alert(shared_lock=shared_lock)
thsObj = ths.Ths(shared_lock=shared_lock)


# 解析新增内容的方法，获取第一列作为股票代码
def parse_content(content):
    columns = content.split(' ')
    stock_code = columns[0]
    return stock_code


def is_time_to_sell(hour, minute):
    current_time = datetime.datetime.now().time()
    target_time = datetime.time(hour, minute)  # 目标时间下午2点50分
    if current_time.hour == target_time.hour and current_time.minute == target_time.minute:
        return True
    else:
        return False


# 开盘时间
def is_deal_time():
    now = datetime.datetime.now()
    if (now.hour == 9 and now.minute >= 27) or (now.hour == 10 and now.minute <= 40):
        return True
    else:
        return False


# 监听文件变化的方法
def watch_file(path, share_lock):
    if not os.path.exists(path):
        # 文件不存在，创建文件
        with open(path, 'w', encoding="utf-8") as file:
            pass
    file = open(path)
    while True:
        if is_time_to_sell(10, 45):
            # 执行开盘卖出策略
            print("当前时间是上午10点55分，取消所有挂单")
            thsObj.quxiao()
            jg.Jiaogedan().clear_sell()
        elif is_deal_time():
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(5)
                file.seek(where)
                mssObj.call_tdx_alert()
            else:
                parsed_code = parse_content(line)
                if len(parsed_code) != 6:
                    print(f"{parsed_code} code 错误")
                    continue
                else:
                    if rule.fitTicket(parsed_code):
                        with share_lock:
                            mssObj.click_soft()
                            purple_price, gray_price_up, gray_price_down = alertObj.purple_price(parsed_code)
                            if purple_price == 0 and gray_price_up == 0 and gray_price_down == 0:
                                # 超过最大尝试次数仍未获取到非零的price1
                                # 在这里处理相应逻辑
                                print(f"获取{parsed_code}的紫色线价格失败")
                            else:
                                current = ticket.TicketInfo().get_realtime_ticket_info(parsed_code)
                                if current == 0:
                                    continue
                                if current <= gray_price_down and gray_price_down != 0:
                                    thsObj.buy(parsed_code, current)
                                elif current < purple_price and current > gray_price_up and purple_price != 0 and gray_price_up != 0:
                                    thsObj.buy(parsed_code, gray_price_up)
                                elif current < gray_price_up and gray_price_up != 0:
                                    thsObj.buy(parsed_code, current)
                                else:
                                    thsObj.buy(parsed_code, purple_price)


if __name__ == '__main__':
    # 读取概念信息
    # df = pd.read_excel('股票行业、板块信息.xlsx',converters={'代码': str})
    # conceptMap = df.set_index('代码').T.to_dict()
    # 将热点板块信息读取到内存
    # f = open("recent_industry_concept.txt",encoding='utf-8')
    # recentIndustryConceptList = f.read().splitlines()
    # f.close()

    # t1 = threading.Thread(watch_file('预警.txt',shared_lock))
    # t1.start()


    thsObj.open_position()
    t2 = threading.Thread(thsObj.sell_strategy())
    t2.start()

    # t1.join()
    t2.join()

    # try:
    #     watch_file('预警.txt')
    # except Exception as e:
    #     msg.dingding.send_msg(f"股票交易自动停止了\r\n{e}")
