
# 交接单记录买卖code，避免多次买卖
class Jiaogedan(object):
    def __init__(self):
        self.__buy_path = "买入.txt"
        self.__sell_path = "卖出.txt"
    # 实现单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Jiaogedan, "_instance"):
            Jiaogedan._instance = object.__new__(cls)
        return Jiaogedan._instance

    #记录已经买入的code
    def record_buy(self,code):
        with open(self.__buy_path, 'a',encoding="utf-8") as f:
            f.write(code)
            f.write('\n')
    # 记录已经卖出的code
    def record_sell(self,code):
        with open(self.__sell_path, 'a',encoding="utf-8") as f:
            f.write(code)
            f.write('\n')
    # 判断是否已经买入
    def is_buyed(self,code):
        with open(self.__buy_path, 'r',encoding="utf-8") as f:
            for line in f.readlines():
                if code in line:
                    return True
        return False
    # 判断是否已经卖出
    def is_selled(self,code):
        with open(self.__sell_path, 'r',encoding="utf-8") as f:
            for line in f.readlines():
                if code in line:
                    return True
        return False
    # 清空买入记录
    def clear_buy(self):
        with open(self.__buy_path, 'w',encoding="utf-8") as f:
            f.write('')
    # 清空卖出记录
    def clear_sell(self):
        with open(self.__sell_path, 'w',encoding="utf-8") as f:
            f.write('')
    # 清空所有记录
    def clear_all(self):
        self.clear_buy()
        self.clear_sell()

if __name__ == '__main__':
    j = Jiaogedan()
    j.clear_all()

