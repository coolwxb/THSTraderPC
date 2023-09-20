import time

import pywinauto
import pyautogui
import easyocr
from pywinauto import keyboard
import re


class Alert(object):
    '''
    通达信预警后执行买入策略
    '''
    def __init__(self):
        self.__app = pywinauto.Application(backend='uia').connect(path = r'E:\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）0807\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）\tdxw.exe')
        # self.__app = pywinauto.Application(backend='uia').connect(process=13388)
    # 监控预警调用查询股票紫色线价格
    def purple_price(self,code):
        # 遍历当前所有窗标题，找到标题包含埋伏主升浪战法的窗口
        w = self.__app.windows()[0]
        # 将窗口置顶
        w.set_focus()
        # 使用pyweinauto 模拟键盘输入code
        keyboard.send_keys(code)
        keyboard.send_keys('{ENTER}')
        # 等待1秒
        time.sleep(1)
        # ocr 截取指定区域图片，解析图片中文本内容
        pyautogui.screenshot(f'pic/{code}.png', region=(1367, 54, 450, 30))
        pyautogui.screenshot(f'pic/{code}-concept.png', region=(0, 910, 1400, 30))
        price1, price2 ,price3 = self.catch_image_for_price(code)

        return price1, price2,price3

    # 解析图片
    def catch_image_for_price(self, code):
        # 使用easyocr 识别图片中文本内容
        reader = easyocr.Reader(['ch_sim', 'en'])
        try:
            result = reader.readtext(f'pic/{code}.png')
            # 使用正则表达式匹配冒号后的数值
            matches = re.findall(r'(\w+):([\d.]+)', result[0][1])
            # 构建字典，按照元组的第一个元素作为键，第二个元素作为值
            result = {key: float(value) for key, value in matches}
            # 打印紫实线和灰下的数值
            v1 = result.get('紫实线')
            v2 = result.get('灰上')
            v3 = result.get('灰下')
            print(f'{code},紫实线：{v1}，灰上：{v2},灰下：{v3}')
            if v1==None:
                v1 = 0
            if v2==None:
                v2 = 0
            if v3==None:
                v3 = 0
            # 返回紫实线的数值
            return v1,v2,v3
        except Exception as e:
            print(e)
            return 0,0


if __name__ == '__main__':
    # w = pywinauto.Application(backend='uia').connect(path = r'E:\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）0807\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）\tdxw.exe')
    # print(w.windows()[0].window_text())
    Alert().purple_price('600300')