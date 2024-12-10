import time

import pywinauto
import pyautogui
import easyocr
from pywinauto import keyboard
import re


class Alert(object):
    # def __init__(self, shared_lock):
    #     self.lock = shared_lock

    '''
    通达信预警后执行买入策略
    '''

    def __init__(self, shared_lock):
        self.lock = shared_lock
        # self.__app = pywinauto.Application(backend='uia').connect(path = r'E:\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）\tdxw.exe')
        # self.__app = pywinauto.Application(backend='uia').connect(process=13388)

    # 监控预警调用查询股票紫色线价格
    def purple_price(self, code):
        # 遍历当前所有窗标题，找到标题包含埋伏主升浪战法的窗口
        # w = self.__app.windows()[0]
        # handles = findwindows.find_windows(process=self.__app.process)
        # w = self.__app.window(handle=handles[0])
        # time.sleep(0.5)
        # # 将窗口置顶
        # w.set_focus()
        # 使用pyweinauto 模拟键盘输入code
        pywinauto.keyboard.send_keys(code)
        # keyboard.send_keys(code)
        pywinauto.keyboard.send_keys('{ENTER}')
        # 等待1秒
        time.sleep(2)
        # ocr 截取指定区域图片，解析图片中文本内容
        pyautogui.screenshot(f'pic/{code}.png', region=(615, 42, 600, 30))
        # self.scalePic(p1,f'pic/{code}.png')
        # p2 = pyautogui.screenshot(f'pic/{code}-concept.png', region=(0, 940, 1400, 30))
        # self.scalePic(p2, f'pic/{code}-concept.png')
        max_attempts = 3
        attempt = 1
        while attempt <= max_attempts:
            purple_up, purple, gray_up, gray_down = self.catch_image_for_price_local(code)
            if purple != 0:
                break
            else:
                pyautogui.screenshot(f'pic/{code}.png', region=(615, 42, 600, 30))
                purple_up, purple, gray_up, gray_down = self.catch_image_for_price_local(code)
                if purple != 0:
                    break
            attempt += 1
        if purple == None:
            if gray_up > 0:
                purple = gray_up
            elif gray_down > 0:
                purple = gray_down
            else:
                purple = 0
        if gray_up == None:
            if gray_down > 0:
                gray_up = gray_down
            elif purple > 0:
                gray_up = purple
            else:
                gray_up = 0
        if gray_down == None:
            if gray_up > 0:
                gray_down = gray_up
            elif purple > 0:
                gray_down = purple
            else:
                gray_down = 0

        return purple_up, purple, gray_up, gray_down

    # 解析图片
    # def catch_image_for_price_api(self, code):
    # 使用easyocr 识别图片中文本内容
    # reader = easyocr.Reader(['ch_sim', 'en'])
    # try:
    #     # result = reader.readtext(f'pic/{code}.png')
    #     # matches = re.findall(r'([\u4e00-\u9fa5]+)：([\d.]+)', result[0][1])
    #     # print(matches)
    #
    #     payload = baidu_ocr.get_file_content_as_base64(f'pic/{code}.png', True)
    #     response = baidu_ocr.baidu_ocr(payload)
    #     if "error_code" in response:
    #         print(response["error_msg"])
    #         return 0, 0, 0
    #     # 使用正则表达式匹配冒号后的数值
    #     if "words_result" in response and len(response["words_result"]) > 0:
    #         for dic in response["words_result"]:
    #
    #             if "words" in dic:
    #                 p = dic['words']
    #                 matches = re.findall(r'(\w+)：([\d+\.\d+]+)', p)
    #                 # 构建字典，按照元组的第一个元素作为键，第二个元素作为值
    #                 result = {key: value for key, value in matches}
    #                 v0 = 0
    #                 v1 = 0
    #                 v2 = 0
    #                 v3 = 0
    #                 # 遍历result
    #                 for k in result:
    #                     if "紫实线" in k:
    #                         v1 = result.get(k)
    #                     elif "灰上" in k:
    #                         v2 = result.get(k)
    #                     elif "灰下" in k:
    #                         v3 = result.get(k)
    #                     elif "紫虚线" in k:
    #                         v0 = result.get(k)
    #
    #                 print(f'{code},紫虚线：{v0}，紫实线：{v1}，灰上：{v2},灰下：{v3}')
    #                 if v0 == None:
    #                     v0 = 0
    #                 if v1 == None:
    #                     v1 = 0
    #                 if v2 == None:
    #                     v2 = 0
    #                 if v3 == None:
    #                     v3 = 0
    #                 # 返回紫实线的数值
    #                 return float(v0),float(v1), float(v2), float(v3)
    #     if "error_msg" in response:
    #         print(f"百度识别ocr报错： {response['error_msg']}")
    # except Exception as e:
    #     print(e)
    #     return 0, 0, 0,0

    def catch_image_for_price_local(self, code):
        # 使用easyocr 识别图片中文本内容
        reader = easyocr.Reader(['ch_sim', 'en'])
        try:
            result = reader.readtext(f'pic/{code}.png')
            pattern = r"(?P<key>[\u4e00-\u9fa5a-zA-Z]+)[:：]\s*(?P<value>\d+(?:\.\d+)?)"
            # 使用正则表达式匹配冒号后的数值
            matches = re.findall(pattern, result[0][1])
            # 构建字典，按照元组的第一个元素作为键，第二个元素作为值
            dic = {key: value for key, value in matches}
            # 打印紫实线和灰下的数值
            v0 = 0
            v1 = 0
            v2 = 0
            v3 = 0
            # 遍历result
            for k in dic:
                if "紫实线" in k:
                    v1 = dic.get(k)
                elif "灰上" in k:
                    v2 = dic.get(k)
                elif "灰下" in k:
                    v3 = dic.get(k)
                elif "紫虚线" in k:
                    v0 = dic.get(k)

            print(f'{code},紫虚线{v0},紫实线：{v1}，灰上：{v2},灰下：{v3}')
            if v0 == None:
                v0 = 0
            if v1 == None:
                v1 = 0
            if v2 == None:
                v2 = 0
            if v3 == None:
                v3 = 0
            # 返回紫实线的数值
            return float(v0), float(v1), float(v2), float(v3)
        except Exception as e:
            print(e)
            return 0, 0, 0, 0


if __name__ == '__main__':
    # w = pywinauto.Application(backend='uia').connect(path = r'E:\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）0807\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）\tdxw.exe')
    # print(w.windows()[0].window_text())
    # Alert().purple_price('600300')
    Alert().catch_image_for_price_local('000524')
