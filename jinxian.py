import os
from datetime import datetime
import pandas as pd
import alert
import ticket
import akshare as ak
import re

from decimal import Decimal

# 金线股统计割肉系统胜率
class Jinxian():

    code = ""
    zise_price= 0
    huise_price = 0
    huise2_price = 0
    shoupan_price= 0
    chajia = 0
    chajia1 = 0
    chajia2 = 0
    yingkui = 0
    buy_date = ""
    sell_date = ""
    chufa = False

dic = {}

# 开盘前记录金线股价格
def record_start():
    # 读取code.txt文件，将每行的内容组成数组
    f = open("code.txt")
    codes = f.read().splitlines()
    f.close()
    for code in codes:
        max_attempts = 3
        attempt = 1
        price1 = 0
        while attempt <= max_attempts:
            # 统计每个金线股的紫色线价格
            price1, price2,price3 = alert.Alert().purple_price(code)
            if price1 != 0 and re.match(r"\d+\.\d{2}$", str(price1)):
                break
            attempt += 1

        if price1 == 0 or not re.match(r"\d+\.\d{2}$", str(price1)):
            # 超过最大尝试次数仍未获取到非零的price1
            # 在这里处理相应逻辑
            print(f"获取{code}的紫色线价格失败")
            with open("紫色线获取失败.txt", 'a') as f:
                f.writelines(code+'\n')
            continue
        else:
            # 输出当日日期，格式化为2021-01-01
            j = Jinxian()
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y%m%d")
            j.code = code
            j.zise_price = price1
            j.huise_price = price2
            j.huise2_price = price3
            j.buy_date = formatted_time
            dic[code] = j

    # 将dic 输出到excel
    path = "金线股.xlsx"
    if os.path.exists(path):
        writer = pd.ExcelWriter(path, engine="openpyxl", mode="a", if_sheet_exists="replace")
        # 存在文件，则追加数据
        df = pd.read_excel(path,converters={'代码': str})

        for key in dic:
            j = dic[key]
            df = df.append(
                {'代码': j.code, '紫色线': j.zise_price, '灰色线': j.huise_price,'灰色线2':j.huise2_price, '收盘价': 0, '差价': 0,'灰色1-收盘':0,'灰色2-收盘':0,'紫色触发': False,
                 '盈亏': 0, '买入日期': j.buy_date, '卖出日期': ""},
                ignore_index=True)
            df.to_excel(writer, index=False)
            writer.save()
    else:
        df = pd.DataFrame(
            columns=['代码', '紫色线', '灰色线','灰色线2', '收盘价', '差价', '触发', '盈亏', '买入日期', '卖出日期'])
        for key in dic:
            j = dic[key]
            df = df.append(
                {'代码': j.code, '紫色线': j.zise_price, '灰色线': j.huise_price,'灰色线2': j.huise2_price, '收盘价': 0, '差价': 0, '触发': False,
                 '盈亏': 0, '买入日期': j.buy_date, '卖出日期': ""},
                ignore_index=True)
        df.to_excel('金线股.xlsx')

# 收盘后记录金线股价格
def record_end():
    #读取金线股信息
    f = open("code.txt")
    codes = f.read().splitlines()
    f.close()
    df = pd.read_excel('金线股.xlsx',converters={'代码': str})
    dic = df.set_index('代码').T.to_dict()
    for code in codes:
        # akshare 获取股票价格
        today= datetime.now().strftime("%Y%m%d")
        allTicketdf =  ak.stock_zh_a_hist(symbol=code, period="daily", start_date=today,
                                                              end_date=today, adjust="qfq")
        shoupanjia = allTicketdf.at[0,'收盘']
        zuidijia = allTicketdf.at[0,'最低']
        zuigao = allTicketdf.at[0,'最高']
        zhangdiefu = allTicketdf.at[0,'涨跌幅']
        # 获取金线股信息
        # 如果dic[] 不存在code，则跳过
        if code not in dic:
            continue
        j = dic[code]
        # 计算差价
        j['差价'] = Decimal(str(shoupanjia)) - Decimal(str(j['紫色线']))
        # 计算盈亏
        try:
            j['盈亏'] = f"{round((Decimal(str(shoupanjia)) - Decimal(str(j['紫色线']))) * 100 /  Decimal(str(j['紫色线'])),2)}%"
        except Exception as e:
            j['盈亏'] = 0
        # 记录收盘价
        j['收盘价'] = shoupanjia
        if zuidijia<= j['紫色线']:
            j['触发'] = True
        j['最高'] = zuigao
        j['最低'] = zuidijia
        j['涨跌幅'] = zhangdiefu
        # 记录日期
        j['卖出日期'] = today
    # 将dic 更新输出到excel
    df = pd.DataFrame(columns=['代码', '紫色线', '灰色线','最高','最低','收盘价','差价','触发','涨跌幅','盈亏','买入日期','卖出日期'])
    for key in dic:
        j = dic[key]
        try:
            df = df.append({'代码': key, '紫色线': j['紫色线'], '灰色线': j['灰色线'], '最高':j['最高'], '最低':j['最低'],'收盘价':j['收盘价'],'差价':j['差价'],'触发':j['触发'],'涨跌幅':j['涨跌幅'],'盈亏':j['盈亏'],'买入日期':j['买入日期'],'卖出日期':j['卖出日期']},
                       ignore_index=True)
        except Exception as e:
            print(e)
    df.to_excel('金线股.xlsx')

if __name__ == '__main__':
    # record_start()
    record_end()
    # datetime.strftime("%Y%m%d")
    # print(datetime.now().strftime("%Y%m%d"))

    # today = datetime.now().strftime("%Y%m%d")
    # # 可当做查询实时股票价格
    # allTicketdf = ak.stock_zh_a_hist(symbol="002281", period="daily", start_date=today,
    #                                  end_date=today, adjust="qfq")
    # print(allTicketdf)


