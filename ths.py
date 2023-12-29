import time
from datetime import datetime, timedelta

import jqktrader
from jqktrader import grid_strategies
import jiaogedan
import alert
import akshare

import msg.dingding
import xline


# 同花顺交易接口封装
class Ths:
    def __init__(self, shared_lock):
        self.lock = shared_lock
        self.open_position_flag = True
        self.dictmap = {}
        self.user = jqktrader.use()
        self.user.connect(
            exe_path=r'E:\同花顺软件\同花顺\xiadan.exe',
            tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        )

    # 单例模式


    # 买入
    def buy(self, code, price):
        if price <= 0:
            return
        # 交接单记录买卖code，避免多次买卖
        if jiaogedan.Jiaogedan().is_buyed(code):
            print(f"已经买入过，不再买入,{code}")
            return

        self.user.refresh()
        # 按照资金比例买入
        data = self.user.balance
        # 获取总资产和资金余额的数值
        total_assets = data['总资产']
        available_funds = data['可用金额']

        # 每股股票的价格和每份股票的数量
        stock_price = price
        shares_per_purchase = 100
        # 分割总资产为10等份，并计算每份的金额
        purchase_amount = total_assets / 20
        # 确保每次购买的股票金额不超过资金余额
        purchase_amount = min(purchase_amount, available_funds)
        # 计算每次购买的股票数量
        shares_to_purchase = int(purchase_amount / stock_price / shares_per_purchase) * shares_per_purchase
        if shares_to_purchase == 0 and shares_per_purchase * stock_price > purchase_amount:
            shares_to_purchase = 100

        # shares_to_purchase = 100
        # 打印购买的股票数量和金额
        print(f"购买股票数量: {shares_to_purchase}")
        print(f"购买股票金额: {shares_to_purchase * stock_price}")
        if shares_to_purchase > 0:
            # 调用买入方法
            try:
                self.user.buy(code, price, shares_to_purchase)
                # 记录已经买入的code
                jiaogedan.Jiaogedan().record_buy(code)
            except Exception as e:
                print(f"买入失败,{code},{e}")
        else:
            print(f"没有足够的资金购买股票,{code}")
    def open_position(self):
        if self.open_position_flag:
            with self.lock:
                self.open_position_flag = False
                self.user.refresh()
                self.user.grid_strategy = jqktrader.grid_strategies.WMCopy()
                po = self.user.position
                print(f"持仓信息：{po}")
                # 对持仓信息进行遍历
                for item in po:
                    # 获取股票可用余额
                    available = item['可用余额']
                    if available > 0:
                        self.dictmap[item['证券代码']] = item

        # 卖出策略

    def sell_strategy(self):
        while True:
            with self.lock:
                self.user.refresh()
                self.user.grid_strategy = jqktrader.grid_strategies.WMCopy()
                po = self.user.position
                for item in po:
                    # 获取股票数量
                    shares = item['可用余额']
                    if shares == 0:
                        continue
                    # 获取股票价格
                    price = item['市价']
                    open_item = self.dictmap[item['证券代码']]
                    stock_name = self.dictmap[item['证券名称']]
                    open_yingli = open_item["盈亏"]
                    now_yingli = item["盈亏"]
                    open_yingkui_ratio = open_item['盈亏比例(%)']
                    now_yingkui_ratio = item['盈亏比例(%)']
                    code = item['证券代码']

                    # 利用x线判断涨幅
                    if xline.X_line(code):
                        print(f"{code} {stock_name}当前价格低于X线，执行卖出操作")
                        msg.dingding.send_msg(f"{code}:{stock_name} 当前价格低于X线，执行卖出操作")
                        self.user.sell(code, price, shares)
                        jiaogedan.Jiaogedan().record_sell(code)
                    else:
                        # 获取昨日最低价
                        # 获取当前日期时间对象
                        now = datetime.now()
                        # 扣除一天以获取昨日日期
                        yesterday = now - timedelta(days=1)
                        # 格式化日期
                        formatted_yesterday = yesterday.strftime('%Y%m%d')
                        now = datetime.now()
                        # 扣除一天以获取昨日日期
                        yesterday = now - timedelta(days=1)
                        # 格式化日期
                        formatted_yesterday = yesterday.strftime('%Y%m%d')

                        allTicketdf = akshare.stock_zh_a_hist(symbol=code, period="daily",
                                                              start_date=formatted_yesterday,
                                                              end_date=formatted_yesterday,
                                                              adjust="qfq")
                        low_price = allTicketdf.iloc[0]['最低']
                        zhangdiefu = allTicketdf.iloc[0]['涨跌幅']

                        if not jiaogedan.Jiaogedan().is_selled(code):
                            # 曾经盈利的股票，下跌到只赚100元时候无脑卖出
                            if (open_yingli > 0 and open_yingli > 100) and now_yingli < 100:
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 曾经盈利的股票，下跌到只赚100元时候无脑卖出")
                            # 曾经盈利的股票，出现亏损100元时候无脑卖出
                            elif open_yingli > 0 and now_yingli < -100:
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 曾经盈利的股票，出现亏损100元时候无脑卖出")
                            # 曾经盈利的股票，出现亏损3%时候无脑卖出
                            elif now_yingkui_ratio < -2.5:
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 曾经盈利的股票，出现亏损3%时候无脑卖出")
                            # 跌破买入当天最低价，无脑卖出
                            elif item['市价'] < low_price:
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 跌破买入当天最低价，无脑卖出")
                            # 利润回撤2个点，无脑卖出
                            elif open_yingkui_ratio > 0 and (
                                    open_yingkui_ratio - 2 > open_yingkui_ratio + now_yingkui_ratio):
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 利润回撤2个点，无脑卖出")
                            # 利润超过8个点，并且当日未涨停，无脑卖出
                            elif now_yingkui_ratio > 8 and zhangdiefu < 9.5:
                                # 卖出
                                self.user.sell(code, price, shares)
                                jiaogedan.Jiaogedan().record_sell(code)
                                msg.dingding.send_msg(f"{code}:{stock_name} 利润超过8个点，并且当日未涨停，无脑卖出")

            print("执行卖出策略")


    # 取消所有委托
    def quxiao(self):
        with self.lock:
            self.user.refresh()
            po = self.user.cancel_all_entrusts()
            print(f"取消所有委托：{po}")
            msg.dingding.send_msg(f"{po}")


# 获取当日成交
def chengjiao(self):
    self.user.refresh()
    self.user.grid_strategy = jqktrader.grid_strategies.Xls()
    po = self.user.deal
    print(f"当日成交：{po}")


def calculate_buying_fee(self, price, quantity):
    # 计算买入手续费
    commission_rate = 0.0003  # 佣金费率
    commission = max(5, price * quantity * commission_rate)  # 佣金最低收费5元
    return commission


def calculate_selling_fee(self, price, quantity):
    # 计算卖出手续费
    commission_rate = 0.0003  # 佣金费率
    commission = max(5, price * quantity * commission_rate)  # 佣金最低收费5元
    tax_rate = 0.001  # 印花税费率
    tax = price * quantity * tax_rate  # 印花税
    return commission + tax


if __name__ == '__main__':
    pass
    # Ths().sell()
