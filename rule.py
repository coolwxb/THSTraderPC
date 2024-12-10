import akshare as ak
import pandas as pd
import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt
import msg.dingding


def fitTicket(stock_code,stock_name):
    # msg.dingding.send_msg(f"开始分析{stock_code}")
    df = getTicetDf(stock_code)
    flag1 = calculate_increase(df, 55)
    flag2 = check_long_shadow_after_limit_up(df)
    # print(flag2)
    # flag3 = has_consecutive_limit_up(df)
    if flag2 == False and flag1 == False:
        print("符合低吸条件")
        msg.dingding.send_msg(f"{stock_code} {stock_name} 符合低吸条件")
        return True
    else:
        print("不符合低吸条件")
        msg.dingding.send_msg(f"{stock_code} {stock_name} 不符合低吸条件")

def getTicetDf(stock_code):
    now = datetime.date.today().strftime('%Y%m%d')
    start_date = pd.to_datetime(now) - pd.Timedelta(days=20)
    formatted_start_date = start_date.strftime('%Y%m%d')
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=formatted_start_date,
                                            end_date=now, adjust="qfq")

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
        print(
            f"最低点日期：{max_increase_low_date.strftime('%Y-%m-%d')}, 最高点日期：{max_increase_high_date.strftime('%Y-%m-%d')}, 涨幅：{max_increase:.2f}%")
        if max_increase > increase_range:
            print(f"累计涨幅超过{increase_range}%,达到{max_increase}%")
            # msg.dingding.send_msg(f"累计涨幅超过{increase_range}%,达到{max_increase}%")
        else:
            print(f"1、累计涨幅不超过{increase_range}%")
            # msg.dingding.send_msg(f"1、累计涨幅不超过{increase_range}%")
        return False
    else:
        print(f"1、累计涨幅不超过{increase_range}%")
        # msg.dingding.send_msg(f"1、累计涨幅不超过{increase_range}%")
        return False


# 检查涨停板之后的两个交易日是否出现长柱阴线
def check_long_shadow_after_limit_up(stock_data):
    # 设置涨停板幅度
    limit_up_ratio = 9.7  # 假设涨停板为10%
    # 阴线实体的比例阈值
    long_candle_body_ratio = 0.50
    # # 开盘高于前一日收盘的阈值
    # open_up_ratio = 1.03
    a, b,high_index = 0, 0,0

    # 遍历交易数据
    for i in range(len(stock_data)):

        # 判断是否是涨停板
        if stock_data.iloc[i]['涨跌幅'] > 0 and (stock_data.iloc[i]['涨跌幅']) >= limit_up_ratio:
            high_index = i
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
            if  candle_body_length > 0:
                daily_range = high_price - low_price
                if daily_range > 0 and (candle_body_length / daily_range) >= long_candle_body_ratio:
                    date = stock_data.iloc[j]['日期']
                    print(f"发现长柱阴线实体: 涨停板日期 {stock_data.iloc[high_index]['日期']}，长柱阴线日期 {date}")
                    # msg.dingding.send_msg(f"发现长柱阴线实体: 涨停板日期 {stock_data.iloc[high_index]['日期']}，长柱阴线日期 {date}")
                    # 格式化数据为 mplfinance 可以使用的格式
                    # 查看数据的列名和前几行，确保数据结构正确
                    # print(stock_data.head())
                    #
                    # # 将 'trade_date' 列转换为 datetime 类型
                    # stock_data['日期'] = pd.to_datetime(stock_data['日期'])
                    #
                    # # 设置 'trade_date' 为索引，并确保索引是 DatetimeIndex
                    # stock_data.set_index('日期', inplace=True)
                    # stock_data = stock_data.rename(
                    #     columns={'日期': 'date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', '最低': 'Low',
                    #              '成交量': 'Volume'})
                    # market_colors = mpf.make_marketcolors(up='red', down='green', inherit=True)
                    # style = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=market_colors)
                    # mpf.plot(stock_data, type='candle', style=style, title=f"Stock K-line for", ylabel='Price',
                    #          figsize=(10, 6))

                    # 显示图形
                    # plt.show()
                    return True
    print("2、未发现高开墓碑")
    # msg.dingding.send_msg("2、未发现高开墓碑")
    # 使用mplfinance绘制K线图

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
                msg.dingding.send_msg("连续3天存在涨停")
                print("连续3天存在涨停")
                msg.dingding.send_msg("连续3天存在涨停")
                # print(stock_zh_a_hist_df.head())
                #
                # # 将 'trade_date' 列转换为 datetime 类型
                # stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
                #
                # # 设置 'trade_date' 为索引，并确保索引是 DatetimeIndex
                # stock_zh_a_hist_df.set_index('日期', inplace=True)
                # stock_data = stock_zh_a_hist_df.rename(
                #     columns={'日期': 'date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', '最低': 'Low',
                #              '成交量': 'Volume'})
                # market_colors = mpf.make_marketcolors(up='red', down='green', inherit=True)
                # style = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=market_colors)
                # mpf.plot(stock_data, type='candle', style=style, title=f"Stock K-line for", ylabel='Price',
                #          figsize=(10, 6))

                # 显示图形
                # plt.show()
                return True
        else:
            consecutive_days_10 = 0
        # 判断是否20%涨停
        if increase_percentage >= 19.5:
            consecutive_days_20 += 1
            if consecutive_days_20 >= 3:  # 连续两天或以上
                print("连续3天存在涨停")
                msg.dingding.send_msg("连续3天存在涨停")
                # print(stock_zh_a_hist_df.head())
                #
                # # 将 'trade_date' 列转换为 datetime 类型
                # stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
                #
                # # 设置 'trade_date' 为索引，并确保索引是 DatetimeIndex
                # stock_zh_a_hist_df.set_index('日期', inplace=True)
                # stock_data = stock_zh_a_hist_df.rename(
                #     columns={'日期': 'date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', '最低': 'Low',
                #              '成交量': 'Volume'})
                # market_colors = mpf.make_marketcolors(up='red', down='green', inherit=True)
                # style = mpf.make_mpf_style(base_mpf_style='charles', marketcolors=market_colors)
                # mpf.plot(stock_data, type='candle', style=style, title=f"Stock K-line for", ylabel='Price',
                #          figsize=(10, 6))

                # 显示图形
                # plt.show()
                return True
        else:
            consecutive_days_20 = 0
    print("3、未出现3日连续涨停")
    msg.dingding.send_msg("3、未出现3日连续涨停")
    return False
#
# df = getTicetDf("000712")
# fitTicket("000712")
