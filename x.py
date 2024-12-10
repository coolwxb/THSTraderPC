import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
from datetime import datetime, timedelta
import akshare as ak


def X_line(code):
    # Fetching the stock data
    now = datetime.now()
    formatted_end = now.strftime('%Y%m%d')

    # Getting data for the last 30 days
    yesterday = now - timedelta(days=30)
    formatted_start = yesterday.strftime('%Y%m%d')

    stock_data = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=formatted_start,
                                    end_date="20241128", adjust="qfq")

    stock_data['日期'] = pd.to_datetime(stock_data['日期'])  # Convert '日期' to datetime

    # Get the second to last row (for yesterday's data)
    thirteenth_trading_day = stock_data.iloc[-2]
    thirteenth_low_price = thirteenth_trading_day['最低']

    # Filter days where the lowest price is less than yesterday's low
    lower_days = stock_data[(stock_data['日期'] < thirteenth_trading_day['日期']) &
                            (stock_data['最低'] < thirteenth_low_price)]

    slopes = []
    for index, row in lower_days.iterrows():
        delta_days = (thirteenth_trading_day['日期'] - row['日期']).days
        slope = (thirteenth_low_price - row['最低']) / delta_days
        sub_price = thirteenth_low_price - row['最低']
        slopes.append((slope, row['日期'], sub_price, delta_days, row['最低']))

    if not slopes:
        print("没有低于昨日最低价的交易日。")
        return

    # Find the lowest (most negative) slope
    lowest_slope, lowest_slope_date, sub_price, delta_days, ori_price = min(slopes, key=lambda x: x[0])

    # Predict the 14th day low based on the slope
    expected_fourteenth_low = sub_price + lowest_slope + ori_price
    nowdf = stock_data.iloc[-1]
    actual_fourteenth_low = nowdf['最低']
    print(f'{code}实时最低价格是：{actual_fourteenth_low:.2f}，预期最低价格是：{expected_fourteenth_low:.2f}')

    # Compare actual lowest price of the 14th day to expected lowest price
    if actual_fourteenth_low < expected_fourteenth_low:
        print(f"交易日的最低价低于昨日最低射线预期值（射线预期值: {expected_fourteenth_low:.2f}）")
        # return True
    else:
        print(f"交易日的最低价高于昨日最低射线预期值（射线预期值: {expected_fourteenth_low:.2f}）")
        # return False

    # ----- Plotting K-line chart with X-line -----

    # Prepare the data for plotting
    # stock_data.set_index('日期', inplace=True)
    # stock_data = stock_data[['开盘', '最高', '最低', '收盘']]  # Selecting the OHLC columns

    # 将 'trade_date' 列转换为 datetime 类型
    stock_data['日期'] = pd.to_datetime(stock_data['日期'])

    # 设置 'trade_date' 为索引，并确保索引是 DatetimeIndex
    stock_data.set_index('日期', inplace=True)
    stock_data = stock_data.rename(
        columns={'日期': 'date', '开盘': 'Open', '收盘': 'Close', '最高': 'High', '最低': 'Low',
                 '成交量': 'Volume'})
    market_colors = mpf.make_marketcolors(up='red', down='green', inherit=True)

    # Create the K-line plot using mplfinance
    apds = []  # List to hold additional plot elements (like X-line)

    # Prepare the X-line (lowest slope) trendline for plotting
    dates = pd.to_datetime([row[1] for row in slopes])  # Dates corresponding to lower days
    predicted_prices = [ori_price + lowest_slope * (thirteenth_trading_day['日期'] - date).days for date in dates]

    # Add the X-line to the plot (using matplotlib)
    fig, axlist = mpf.plot(stock_data, type='candle', style='charles', title=f' K-line Chart',
                           ylabel='Price', ylabel_lower='Volume', volume=True, returnfig=True)

    # Extracting the main axis
    ax = axlist[0]

    # Plot the X-line on top of the K-line chart (candlestick)
    ax.plot(dates, predicted_prices, label='Predicted X-line (Lowest Slope)', color='red', linestyle='--')

    # Customize the plot
    ax.legend(loc='best')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.grid(True)

    plt.xticks(rotation=45)
    plt.show()

X_line("300723")