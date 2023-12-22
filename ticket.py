from datetime import datetime

import akshare as ak
import pyautogui
import pandas as pd
# 获取股票实时信息
# stock_individual_info_em_df = ak.stock_individual_info_em(symbol="603777")
# print(stock_individual_info_em_df)

class TicketInfo(object):
    # 单例模式
    def __new__(cls, *args, **kwargs):
        if not hasattr(TicketInfo, "_instance"):
            TicketInfo._instance = object.__new__(cls)
        return TicketInfo._instance
    # 获取股票实时信息
    def get_stock_individual_info_em(self,code):
        stock_bid_ask_em_df = ak.stock_bid_ask_em(symbol=code)
        return stock_bid_ask_em_df.iloc[8].iat[1]

    # 获取股票概念
    def save_stock_concept(self):
        # 获取所有概念
        stock_concept_df = ak.stock_board_concept_name_ths()
        stock_concept_df.to_excel('概念.xlsx')

    def save_all_ticket(self):
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        stock_zh_a_spot_df.to_excel('股票.xlsx')

    def save_all_board_industry(self):
        stock_board_spot_df = ak.stock_board_industry_summary_ths()
        stock_board_spot_df.to_excel('行业.xlsx')

    # 导出股票行业、概念信息
    def export_industry_concept_xlsx(self):
        self.save_stock_concept()
        self.save_all_board_industry()
        self.save_all_ticket()
        info = pd.read_excel('股票.xlsx')
        dicmap = {}
        # 初始化将股票信息存入字典
        for index, row in info.iterrows():
            info = TicketDetailInfo()
            info.code = row['代码'][2:]
            info.name = row['名称']
            dicmap[info.code] = info
        # 获取股票行业信息
        industry = pd.read_excel('行业.xlsx')
        for index, row in industry.iterrows():
            inudstry_name = row['板块']
            # 获取板块下的所有股票
            stock_board_detail_df = ak.stock_board_industry_cons_ths(symbol=inudstry_name)
            for index, row in stock_board_detail_df.iterrows():
                code = row['代码']
                if code in dicmap.keys():
                    m = dicmap[code]
                    m.industry.append(inudstry_name)

        # 获取股票概念信息
        concept = pd.read_excel('概念.xlsx')
        for index, row in concept.iterrows():
            concept_name = row['概念名称']
            # 获取概念下的所有股票
            stock_board_detail_df = ak.stock_board_concept_cons_ths(symbol=concept_name)
            for index, row in stock_board_detail_df.iterrows():
                code = row['代码']
                if code in dicmap.keys():
                    info = dicmap[code]
                    info.concept.append(concept_name)

        # 将dicmap 输出到excel
        df = pd.DataFrame(columns=['代码', '名称', '行业', '概念'])
        for key in dicmap:
            info = dicmap[key]
            df = df.append({'代码': info.code, '名称': info.name, '行业': info.industry, '概念': info.concept},
                           ignore_index=True)
        df.to_excel('股票行业、板块信息.xlsx')
    # 获取实时股票信息
    def get_realtime_ticket_info(self,code):
        today = datetime.now().strftime("%Y%m%d")
        # 可当做查询实时股票价格
        allTicketdf = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=today,end_date=today, adjust="qfq")
        if allTicketdf.empty==0:
            return 0
        else:
            return allTicketdf.at[0,'收盘']


class TicketDetailInfo(object):
    def __init__(self):
        self.code = '' # 股票代码
        self.name = '' # 股票名称
        self.__industry = [] # 行业
        self.__concept = [] # 概念
    # 行业
    @property
    def industry(self):
        return self.__industry
    @industry.setter
    def industry(self, value):
        self.__industry.append(value)
    # 概念
    @property
    def concept(self):
        return self.__concept
    @concept.setter
    def concept(self, value):
        self.__concept.append(value)






if __name__ == '__main__':
    # print(TicketInfo().get_realtime_ticket_info("603096"))
    TicketInfo().export_industry_concept_xlsx()