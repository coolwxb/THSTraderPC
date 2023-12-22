import akshare as ak
import pandas as pd
import datetime

def fitTicket(stock_code):
    try:
        df = getTicetDf(stock_code)
        flag1 = calculate_increase(df, 35)
        flag2 = check_long_shadow_after_limit_up(df)
        flag3 = has_consecutive_limit_up(df)
        if flag3 == False and flag2 == False and flag1 == False:
            return True
        else:
            print("不符合低吸条件")
    except Exception as e:
        print(stock_code)
        print(e)
def getTicetDf(stock_code):
    now = datetime.date.today().strftime('%Y%m%d')
    start_date = pd.to_datetime(now) - pd.Timedelta(days=30)
    formatted_start_date = start_date.strftime('%Y%m%d')
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=formatted_start_date,adjust="qfq")
    return stock_zh_a_hist_df

# 计算涨幅
def calculate_increase(stock_zh_a_hist_df, increase_range):

    # 确保DataFrame按日期排序
    stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
    stock_zh_a_hist_df.sort_values(by='日期', inplace=True)

    # 获取最近的10个交易日的数据
    recent_10_days = stock_zh_a_hist_df.tail(10)

    # 初始化最大涨幅和对应的最低点与最高点日期
    max_increase = -1
    max_increase_low_date = None
    max_increase_high_date = None

    # 遍历所有可能的最低点和最高点配对
    for i in range(9):
        for j in range(i + 1, 10):
            low_price = recent_10_days.iloc[i]['最低']
            high_price = recent_10_days.iloc[j]['最高']
            low_date = recent_10_days.iloc[i]['日期']
            high_date = recent_10_days.iloc[j]['日期']

            # 计算涨幅并更新最大涨幅
            increase = ((high_price - low_price) / low_price) * 100
            if increase > max_increase:
                max_increase = increase
                max_increase_low_date = low_date
                max_increase_high_date = high_date

    # 最终结果
    if max_increase_low_date and max_increase_high_date:
        print(f"最低点日期：{max_increase_low_date.strftime('%Y-%m-%d')}, 最高点日期：{max_increase_high_date.strftime('%Y-%m-%d')}, 涨幅：{max_increase:.2f}%")
        if max_increase > increase_range:
            print(f"累计涨幅超过{increase_range}%,达到{max_increase}%")
        else:
            print(f"1、累计涨幅不超过{increase_range}%")
        return False
    else:
        print(f"1、累计涨幅不超过{increase_range}%")
        return False

# 检查涨停板之后的两个交易日是否出现长柱阴线
def check_long_shadow_after_limit_up(stock_data):
    # stock_data = stock_zh_a_hist_df.iloc[::-1].reset_index(drop=True)
    # # 设置涨停板幅度
    # limit_up_ratio = 1.10  # 假设涨停板为10%
    # # 阴线实体的比例阈值
    # long_candle_body_ratio = 0.70
    #
    # # 遍历交易数据
    # for i in range(len(stock_data) - 3):
    #     # 判断是否是涨停板
    #     if stock_data.iloc[i + 1]['收盘'] > 0 and (
    #             stock_data.iloc[i]['收盘'] / stock_data.iloc[i + 1]['收盘'] >= limit_up_ratio):
    #         # 在涨停板之后的两个交易日内检查
    #         for j in range(i - 1, i - 3, -1):
    #             open_price = stock_data.iloc[j]['开盘']
    #             close_price = stock_data.iloc[j]['收盘']
    #             high_price = stock_data.iloc[j]['最高']
    #             low_price = stock_data.iloc[j]['最低']
    #
    #             # 计算阴线实体长度
    #             candle_body_length = open_price - close_price
    #             daily_range = high_price - low_price
    #
    #             # 判断是否为长柱阴线
    #             if candle_body_length > 0 and (candle_body_length / daily_range >= long_candle_body_ratio):
    #                 date = stock_data.iloc[j]['日期']
    #                 print(f"发现长柱阴线实体: 涨停板日期 {stock_data.iloc[i]['日期']}，长柱阴线日期 {date}")
    #                 return True
    # print("2、未出现墓碑形态")
    # return False
    # start_date 前推6天的日期


    # 设置涨停板幅度
    limit_up_ratio = 9.7  # 假设涨停板为10%
    # 阴线实体的比例阈值
    long_candle_body_ratio = 0.50
    # 开盘高于前一日收盘的阈值
    open_up_ratio = 1.03

    # 遍历交易数据
    for i in range(len(stock_data)):
        # 判断是否是涨停板
        if stock_data.iloc[i]['涨跌幅'] > 0 and (stock_data.iloc[i]['涨跌幅']) >= limit_up_ratio:
            a, b = 0, 0
            if i + 1 < len(stock_data) and i + 2 < len(stock_data):
                a = i + 1
                b = i + 3
            elif i + 1 < len(stock_data) and i + 2 >= len(stock_data):
                a = i + 1
                b = i + 2
            else:
                continue
            # 在涨停板之后的两个交易日内检查
            for j in range(a, b, 1):
                prev_close_price = stock_data.iloc[j - 1]['收盘']
                open_price = stock_data.iloc[j]['开盘']
                close_price = stock_data.iloc[j]['收盘']
                high_price = stock_data.iloc[j]['最高']
                low_price = stock_data.iloc[j]['最低']
                # 计算阴线实体长度
                candle_body_length = open_price - close_price
                # 判断是否为长柱阴线且开盘价高于前一交易日收盘价3%
                if open_price >= prev_close_price * open_up_ratio and candle_body_length > 0:
                    daily_range = high_price - low_price
                    if daily_range > 0 and (candle_body_length / daily_range) >= long_candle_body_ratio:
                        date = stock_data.iloc[j]['日期']
                        print(f"发现长柱阴线实体: 涨停板日期 {stock_data.iloc[i]['日期']}，长柱阴线日期 {date}")
                        return True
    print("2、未发现高开墓碑")
    return False

# 是否有连续涨停
def has_consecutive_limit_up(stock_zh_a_hist_df):
    # 提取收盘价
    closing_prices = stock_zh_a_hist_df['收盘'].tail(10).tolist()  # 获取最近10个交易日的收盘价
    consecutive_days_10 = 0
    consecutive_days_20 = 0

    for i in range(1, len(closing_prices)):
        # 计算涨幅
        increase_percentage = ((closing_prices[i] - closing_prices[i - 1]) / closing_prices[i - 1]) * 100
        # 判断是否10%涨停
        if increase_percentage >= 9.5:
            consecutive_days_10 += 1
            if consecutive_days_10 >= 3:  # 连续两天或以上
                print("连续3天存在涨停")
                return True
        else:
            consecutive_days_10 = 0
        # 判断是否20%涨停
        if increase_percentage >= 19.5:
            consecutive_days_20 += 1
            if consecutive_days_20 >= 3:  # 连续两天或以上
                print("连续3天存在涨停")
                return True
        else:
            consecutive_days_20 = 0
    print("3、未出现3日连续涨停")
    return False

# df = getTicetDf("600697")
fitTicket("600697")
