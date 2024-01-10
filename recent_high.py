import akshare as ak
from datetime import datetime, timedelta

import pandas as pd
def is_recent_high(stock_code):


    # 获取当前日期，并计算过去 30 天的日期
    end_date = datetime.today().strftime('%Y%m%d')
    start_date = (datetime.today() - timedelta(days=30)).strftime('%Y%m%d')

    # 使用 AkShare 获取股票行情数据
    stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock_code, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")

    # 打印获取的数据（可选）
    # print(stock_zh_a_hist_df)

    # 确保按日期排序（如果需要的话）
    stock_zh_a_hist_df['日期'] = pd.to_datetime(stock_zh_a_hist_df['日期'])
    stock_zh_a_hist_df.sort_values('日期', inplace=True)

    # 获取近 30 天的最高价
    max_price_30d = stock_zh_a_hist_df['最高'].max()

    # 获取最近 5 天内的最高价
    max_price_5d = stock_zh_a_hist_df['最高'][-5:].max()

    # 最近 5 天内的最高价是否是近 30 天中的最高价
    is_max = max_price_5d == max_price_30d

    print(f"近30天的最高价为: {max_price_30d}")
    print(f"近5天的最高价为: {max_price_5d}")
    print(f"最近5天中的最高价{'是' if is_max else '不是'}近30天中的最高价")
    if is_max:
        return True
    else:
        return False