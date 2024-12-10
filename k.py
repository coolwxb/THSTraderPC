
import akshare as ak
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt

# 获取某只股票的日K线数据（以平安银行为例）
stock_code = '300006'  # 平安银行的股票代码
stock_data = ak.stock_zh_a_daily(symbol=stock_code,start_date='20241129',end_date='20241129')

# 格式化数据为 mplfinance 可以使用的格式
stock_data['date'] = pd.to_datetime(stock_data['date'])
stock_data.set_index('date', inplace=True)

# 获取最新一日的K线数据
latest_data = stock_data.iloc[-1]
open_price = latest_data['open']
close_price = latest_data['close']
high_price = latest_data['high']
low_price = latest_data['low']

# 判断墓碑线的条件：
shadow_threshold = 0.01  # 阈值设为1%
upper_shadow = high_price - max(open_price, close_price)  # 上影线
lower_shadow = min(open_price, close_price) - low_price  # 下影线

# 判断条件
is_gravestone_doji = (
    abs(close_price - low_price) / low_price < shadow_threshold and  # 收盘接近最低价
    upper_shadow > 2 * (close_price - open_price) and  # 上影线长
    lower_shadow < 0.1 * (high_price - low_price)  # 下影线短
)

# 打印判断结果
if is_gravestone_doji:
    print("当日K线为墓碑线")
else:
    print("当日K线不是墓碑线")

# 使用mplfinance绘制K线图
mpf.plot(stock_data, type='candle', style='charles', title=f"Stock K-line for {stock_code}", ylabel='Price', figsize=(10, 6))

# 显示图形
plt.show()
