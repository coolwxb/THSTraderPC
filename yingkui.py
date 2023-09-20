# 每日盈亏统计
import os.path

import pandas as pd


# 盈亏统计
class Yingkui(object):
    def __init__(self):
        self.__path = "每日盈亏.xlsx"

    # 到处excel文件
    def export(self, data):
        if os.path.exists(self.__path):
            writer = pd.ExcelWriter(self.__path, engine="openpyxl", mode="a", if_sheet_exists="replace")
            # 存在文件，则追加数据
            df = pd.read_excel(self.__path)
            df = df.append(data, ignore_index=True)
            df.to_excel(writer, index=False)
            writer.save()
        else:
            # 不存在文件，则创建文件
            df = pd.DataFrame(data)
            df.to_excel(self.__path, index=False)
