import jqktrader
from jqktrader import grid_strategies
import jiaogedan
import alert


# 同花顺交易接口封装
class Ths(object):
    def __init__(self):
        self.user = jqktrader.use()
        self.user.connect(
            exe_path=r'E:\同花顺软件\同花顺\xiadan.exe',
            tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        )

    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Ths, "_instance"):
            Ths._instance = object.__new__(cls)
        return Ths._instance

    # 获取持仓信息
    def chicang(self):
        self.user.refresh()
        self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.position
        print(f"持仓信息：{po}")

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
        if shares_to_purchase== 0 and shares_per_purchase* stock_price > purchase_amount:
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

    # 卖出
    def sell(self):
        # 取消所有买入卖出委托，重新挂单
        self.quxiao()
        # 清空卖出记录
        jiaogedan.Jiaogedan().clear_sell()
        self.user.refresh()
        self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.position

        print(f"持仓信息：{po}")
        # 对持仓信息进行遍历
        for item in po:
            # 获取股票可用余额
            available = item['可用余额']
            if available > 0:
                # 判断股票盈亏比例（%） 大于3%卖出
                if item['盈亏比例(%)'] > 3:
                    # 获取股票代码
                    code = item['证券代码']
                    # 获取股票价格
                    price = item['市价']
                    # 获取股票数量
                    shares = item['可用余额']
                    if not jiaogedan.Jiaogedan().is_selled(code):
                        # 卖出
                        self.user.sell(code, price, shares)
                        jiaogedan.Jiaogedan().record_sell(code)
                # 判断股票盈亏比例（%） 小于-3%卖出
                elif item['盈亏比例(%)'] < -3:
                    # 获取股票代码
                    code = item['证券代码']
                    # 获取股票价格
                    price = item['市价']
                    # 获取股票数量
                    shares = item['可用余额']
                    if not jiaogedan.Jiaogedan().is_selled(code):
                        # 卖出
                        self.user.sell(code, price, shares)
                        jiaogedan.Jiaogedan().record_sell(code)
        pass

    # 开盘卖出
    def open_sell(self):
        self.user.refresh()
        self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.position

        print(f"持仓信息：{po}")
        # 对持仓信息进行遍历
        for item in po:
            # 获取股票可用余额
            available = item['可用余额']
            # 获取股票价格
            price = item['市价']
            # 获取股票价格
            chengben = item['成本价']
            # 获取股票代码
            code = item['证券代码']
            # 获取股票数量
            shares = item['可用余额']
            # 亏损 》-3 直接卖
            if available > 0 and item['盈亏比例(%)']<-3 :
                    # 卖出
                self.user.sell(code, price, shares)
                jiaogedan.Jiaogedan().record_sell(code)
            # 亏损《-3 保本卖
            elif available > 0 and item['盈亏比例(%)']> -3 and chengben > price:
                    # 卖出
                self.user.sell(code, chengben+0.1, shares)
                jiaogedan.Jiaogedan().record_sell(code)
            # 有盈利
            elif available > 0 and item['盈亏比例(%)'] > 3 :
                    # 卖出
                self.user.sell(code, price, shares)
                jiaogedan.Jiaogedan().record_sell(code)


    # 获取资金信息
    def zijin(self):
        self.user.refresh()
        self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.balance
        print(f"资金信息：{po}")


    # 获取当日委托
    def weituo(self):
        self.user.refresh()
        self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.entrust
        print(f"当日委托：{po}")
    # 取消所有委托
    def quxiao(self):
        self.user.refresh()
        # self.user.grid_strategy = jqktrader.grid_strategies.Xls()
        po = self.user.cancel_all_entrusts()
        print(f"取消所有委托：{po}")

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
    Ths().sell()
