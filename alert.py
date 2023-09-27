import time

import pywinauto
import pyautogui
import easyocr
from pywinauto import keyboard
from pywinauto import findwindows
import re
import baidu_ocr


class Alert(object):
    '''
    通达信预警后执行买入策略
    '''
    def __init__(self):
        self.__app = pywinauto.Application(backend='uia').connect(path = r'E:\tdx\tdx\tdxw.exe')
        # self.__app = pywinauto.Application(backend='uia').connect(process=13388)
    # 监控预警调用查询股票紫色线价格
    def purple_price(self,code):
        # 遍历当前所有窗标题，找到标题包含埋伏主升浪战法的窗口
        # w = self.__app.windows()[0]
        handles = findwindows.find_windows(process=self.__app.process)
        w = self.__app.window(handle=handles[0])
        time.sleep(0.5)
        # 将窗口置顶
        w.set_focus()

        # 使用pyweinauto 模拟键盘输入code
        keyboard.send_keys(code)
        keyboard.send_keys('{ENTER}')
        # 等待1秒
        time.sleep(1)
        # ocr 截取指定区域图片，解析图片中文本内容
        p1 = pyautogui.screenshot(f'pic/{code}.png', region=(1175, 42, 450, 30))
        # self.scalePic(p1,f'pic/{code}.png')
        p2 = pyautogui.screenshot(f'pic/{code}-concept.png', region=(0, 940, 1400, 30))
        # self.scalePic(p2, f'pic/{code}-concept.png')
        max_attempts = 3
        attempt = 1
        while attempt <= max_attempts:
            price1, price2 ,price3 = self.catch_image_for_price(code)
            if price1 != 0:
                break
            attempt += 1
        if price1 == None:
            if price2>0:
                price1 = price2
            elif price3>0:
                price1 = price3
            else:
                price1 = 0
        if price2 == None:
            if price3 > 0:
                price2 = price3
            elif price1>0:
                price2 = price1
            else:
                price2 = 0
        if price3 == None:
            if price2 > 0:
                price3 = price2
            elif price1 > 0:
                price3 = price1
            else:
                price3 = 0

        return price1, price2,price3
    # def scalePic(self,pic,path):
    #     # 指定放大倍数
    #     scale_factor = 2  # 2倍放大，可以根据需要调整
    #     # 获取截图的宽度和高度
    #     width, height = pic.size
    #     # 计算放大后的宽度和高度
    #     new_width = width * scale_factor
    #     new_height = height * scale_factor
    #     # 使用PIL库对截图进行放大
    #     screenshot = pic.resize((new_width, new_height), resample=Image.BILINEAR)
    #     enhancer = ImageEnhance.Sharpness(screenshot)
    #     factor = 2.0
    #
    #     # 增强图片
    #     img_enhanced = enhancer.enhance(factor)
    #
    #     # 保存放大后的截图
    #     img_enhanced.save(path)
    # 解析图片
    def catch_image_for_price(self, code):
        # 使用easyocr 识别图片中文本内容
        # reader = easyocr.Reader(['ch_sim', 'en'])
        try:
            # result = reader.readtext(f'pic/{code}.png')
            # matches = re.findall(r'([\u4e00-\u9fa5]+)：([\d.]+)', result[0][1])
            # print(matches)

            payload = baidu_ocr.get_file_content_as_base64(f'pic/{code}.png',True)
            response = baidu_ocr.baidu_ocr(payload)
            # 使用正则表达式匹配冒号后的数值
            if "words_result" in response and len(response["words_result"])>0 :
                if "words" in response["words_result"][0]:
                    p = response["words_result"][0]['words']
                    matches = re.findall(r'(\w+)：([\d+\.\d+]+)',p)
                    # 构建字典，按照元组的第一个元素作为键，第二个元素作为值
                    result = {key: value for key, value in matches}
                    v1 = 0
                    v2 = 0
                    v3 = 0
                    # 遍历result
                    for k in result:
                        if "紫实线" in k:
                            v1 = result.get(k)
                        elif "灰上" in k:
                            v2 = result.get(k)
                        elif "灰下" in k:
                            v3 = result.get(k)

                    print(f'{code},紫实线：{v1}，灰上：{v2},灰下：{v3}')
                    if v1==None:
                        v1 = 0
                    if v2==None:
                        v2 = 0
                    if v3==None:
                        v3 = 0
                    # 返回紫实线的数值
                    return float(v1),float(v2),float(v3)
            if "error_msg" in response:
                print(f"百度识别ocr报错： {response['error_msg']}")
        except Exception as e:
            print(e)
            return 0,0,0


if __name__ == '__main__':
    # w = pywinauto.Application(backend='uia').connect(path = r'E:\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）0807\【埋伏主升浪战法】【涨停倍量阴突破战法】二合一版本（免安装版）\tdxw.exe')
    # print(w.windows()[0].window_text())
    Alert().purple_price('600300')