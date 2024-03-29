from datetime import datetime

import akshare as ak


now = datetime.now()
nowstr = now.strftime('%Y-%m-%d')

tool_trade_date_hist_sina_df = ak.tool_trade_date_hist_sina()
index = tool_trade_date_hist_sina_df.loc[tool_trade_date_hist_sina_df['trade_date'] == now.date()].index[0]
t= tool_trade_date_hist_sina_df.iloc[index-1]['trade_date']
print(t)