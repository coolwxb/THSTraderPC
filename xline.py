from datetime import datetime, timedelta

import akshare as ak
import pandas as pd

# 交易实现判断X线
def X_line(code):
    now = datetime.now()
    formatted_end = now.strftime('%Y%m%d')
    # 扣除一天以获取昨日日期
    yesterday = now - timedelta(days=15)
    # 格式化日期
    formatted_start = yesterday.strftime('%Y%m%d')

    stock_data = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=formatted_start,
                                    end_date=formatted_end,
                                    adjust="qfq")

    # 将日期列转换为 datetime 类型
    stock_data['日期'] = pd.to_datetime(stock_data['日期'])

    # 寻找给定日期之前的所有交易日的最低价低于昨日最低价的日期
    thirteenth_trading_day = stock_data.iloc[-2]
    thirteenth_low_price = thirteenth_trading_day['最低']

    # 选择在昨日之前且最低价低于昨日最低价的所有交易日
    lower_days = stock_data[(stock_data['日期'] < thirteenth_trading_day['日期']) &
                            (stock_data['最低'] < thirteenth_low_price)]

    # 计算与昨日最低价之间的射线斜率
    slopes = []
    for index, row in lower_days.iterrows():
        delta_days = (thirteenth_trading_day['日期'] - row['日期']).days
        slope = (thirteenth_low_price - row['最低']) / delta_days
        # 差额
        sub_price = thirteenth_low_price - row['最低']
        # 把每个斜率和对应的日期存起来
        slopes.append((slope, row['日期'], sub_price, delta_days, row['最低']))

    # 如果没有找到比昨日更低的交易日，则没有可比较的射线
    if not slopes:
        print("没有低于昨日最低价的交易日。")
    else:
        # 从所有斜率中找到最低射线的斜率（最负的斜率）
        lowest_slope, lowest_slope_date, sub_price, delta_days, ori_price = min(slopes, key=lambda x: x[0])
        # 后一日射线上点的价格
        expected_fourteenth_low = sub_price + lowest_slope + ori_price
        # 可当做查询实时股票价格
        nowdf = stock_data.iloc[-1]
        actual_fourteenth_low = nowdf['最低']
        print(f'{code}实时最低价格是：{actual_fourteenth_low:.2f}，预期最低价格是：{expected_fourteenth_low:.2f}')

        # 比较第14个交易日的最低价是否低于通过选出最低射线预测的最低价
        if actual_fourteenth_low < expected_fourteenth_low:
            print(f"交易日的最低价低于昨日最低射线预期值（射线预期值: {expected_fourteenth_low:.2f}）")
            return True
        else:
            print(f"交易日的最低价高于昨日最低射线预期值（射线预期值: {expected_fourteenth_low:.2f}）")
            return False
