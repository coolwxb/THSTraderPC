import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 判断趋势是否走坏
def bad_trend (symbol):
    # 获取当天日期
    date = pd.Timestamp.now().strftime("%Y-%m-%d")
    # 获取9点-9点30分之间的实时数据
    # symbol = "002862"
    start_time = f"{date} 09:30:00"
    end_time = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    # end_time = f"{date} 09:34:00"
    data = ak.stock_zh_a_hist_min_em(symbol=symbol, start_date=start_time, end_date=end_time,period="5",adjust="qfq")

    # 提取价格数据
    prices = data["收盘"].tolist()

    # 绘制价格连线图
    x = np.arange(len(prices))
    plt.plot(x, prices)

    # 初始化变量
    trend = []
    first_upward_trend_index = -1
    last_upward_trend_index = -1
    lowest_downtrend_index = -1

    # 寻找转折点，并绘制转折点
    for i in range(0, len(prices) - 1):
        if i==0:
            trend.append(1)
            if first_upward_trend_index == -1:
                first_upward_trend_index = i  # 记录第一个上涨转折点的索引
                plt.plot(x[i], prices[i], 'ro')  # 绘制第一个上涨转折点，使用绿色
            last_upward_trend_index = i  # 更新最后一个上涨转折点的索引
        elif prices[i] > prices[i-1] and prices[i] > prices[i+1]:
            trend.append(1)  # 上涨趋势
            plt.plot(x[i], prices[i], 'ro')  # 绘制第一个上涨转折点，使用绿色
            last_upward_trend_index = i  # 更新最后一个上涨转折点的索引
        elif prices[i] < prices[i-1] and prices[i] < prices[i+1]:
            trend.append(-1)  # 下跌趋势
            if lowest_downtrend_index == -1 or prices[i] < prices[lowest_downtrend_index]:
                lowest_downtrend_index = i  # 更新价格最低的转折点索引


    plt.plot(x[lowest_downtrend_index], prices[lowest_downtrend_index], 'yo', label='下跌趋势价格最低转折点')  # 绘制下跌趋势价格最低转折点，使用黄色

    plt.plot(x[last_upward_trend_index], prices[last_upward_trend_index], 'bo', label='最后一个上涨转折点')  # 绘制最后一个上涨转折点，使用蓝色

    plt.legend()
    plt.show()
    if (prices[last_upward_trend_index] > prices[first_upward_trend_index]):
        print("当前处于上涨趋势")
        return False;
    else:
        print("当前处于下跌趋势")
        # 计算第一个上涨趋势转折点和最后一个转折点之间的绝对值
        first_last_diff = abs(prices[last_upward_trend_index] - prices[first_upward_trend_index])
        # 计算第一个上涨趋势转折点和下跌趋势价格最低的转折点之间的绝对值
        lowest_downtrend_diff = abs(prices[lowest_downtrend_index] - prices[first_upward_trend_index])

        # 计算差值占比
        diff_ratio = first_last_diff / lowest_downtrend_diff * 100
        # 输出结果
        # print("第一个上涨趋势转折点和最后一个转折点之间的差值: {:.2f}".format(first_last_diff))
        # print("第一个上涨趋势转折点和下跌趋势价格最低的转折点之间的差值: {:.2f}".format(lowest_downtrend_diff))
        print("下降趋势差值占比: {:.2f}%".format(diff_ratio))
        if diff_ratio > 30:
            print("反弹无效，下跌趋势走坏")
            return True
        else:
            return False
    # 可视化

bad_trend("002862")