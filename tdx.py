from mootdx.quotes import Quotes

# 标准市场
client = Quotes.factory(market='std', multithread=True, heartbeat=True, bestip=True, timeout=15)

# k 线数据
bars = client.bars(symbol='600036', frequency=9, offset=10)
print(bars)

