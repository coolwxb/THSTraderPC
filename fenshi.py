import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 获取某只股票的分时数据
stock_code = '002889'  # 这里以平安银行为例
df_tick = df = ak.stock_zh_a_hist_min_em(symbol=stock_code, start_date="2024-11-29 09:30:00", end_date="2024-11-29 09:50:00", period="1", adjust="")



# 获取当前的价格和均线
current_price = df_tick['收盘'].iloc[-1]  # 最新的价格
sma_value = df_tick['均价'].iloc[-1]  # 最新的SMA值

# 计算价格与均线的偏移量
offset = current_price - sma_value
offset_percent = (offset / sma_value) * 100

# 打印当前价格与均线的偏移值
print(f"当前价格：{current_price}，分时均线：{sma_value}")
print(f"价格与均线的偏移值：{offset:.2f}，偏移百分比：{offset_percent:.2f}%")

# 绘制分时图及均线
plt.figure(figsize=(10, 6))

# 绘制价格和SMA
plt.plot(df_tick['时间'], df_tick['收盘'], label='价格', color='blue', alpha=0.7, linewidth=1.5)
plt.plot(df_tick['时间'], df_tick['均价'], label='5分钟均线', color='red', linestyle='--', linewidth=1.5)

# 标注当前价格
plt.scatter(df_tick['时间'].iloc[-1], current_price, color='black' , label=f"当前价格 {current_price}", zorder=5)

# 标注SMA值
plt.scatter(df_tick['时间'].iloc[-1], sma_value, color='orange', label=f"当前SMA {sma_value}", zorder=5)

# 添加标题和标签
plt.title(f"股票 {stock_code} 分时图及均线偏移分析", fontsize=16)
plt.xlabel('时间', fontsize=12)
plt.ylabel('价格', fontsize=12)

# 显示图例
plt.legend()

# 显示图形
plt.xticks(rotation=45)  # 使时间标签倾斜，避免重叠
plt.tight_layout()
plt.show()
