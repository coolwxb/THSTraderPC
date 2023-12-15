import jiaogedan


# 每日任务
# 每日3：30 清空交割单、买入卖出记录，预警.txt

class Task(object):
    def __init__(self):
        self.__jiaogedan = jiaogedan.Jiaogedan()
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(Task, "_instance"):
            Task._instance = object.__new__(cls)
        return Task._instance
    # 清空记录
    def clear(self):
        self.__jiaogedan.clear_all()
        with open("预警.txt", 'w') as f:
            f.write('')

    # 每日盈亏统计
    def yingkui(self):
        pass

if __name__ == '__main__':
    t = Task()
    t.clear()



