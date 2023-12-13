import time

import pyautogui
import pywinauto
from mootdx.quotes import Quotes

# 开启通达信软件
def openTDX():


    pywinauto.application.Application(backend='uia').start(r'E:\tdx\tdx\tdxw.exe')
    time.sleep(2)

    # 点击游客登录
    pyautogui.moveTo(1122, 655)
    pyautogui.click()
    print("执行完===点击游客登录")
    time.sleep(1)
    locate = pyautogui.locateOnScreen(r"tdx/btn_guest_sure.png", confidence=0.4, region=(600, 260, 800, 800))
    if locate == None:
        pyautogui.moveTo(410, 1060)
        pyautogui.click()
        print("执行完===点击ico 弹出窗体")
        time.sleep(2)

    # 点击游客登录确定
    pyautogui.moveTo(1122, 65)
    pyautogui.click()
    print("执行完===点击游客登录确定")
    time.sleep(2)


    btn_sure_locate = pyautogui.locateCenterOnScreen(r"tdx/btn_guest_sure.png", confidence=0.4,region=(600,260,800,800))
    if btn_sure_locate!=None:
        pyautogui.moveTo(btn_sure_locate.x,btn_sure_locate.y)
        pyautogui.click()
    # # # 点击确定检测dll
    # pyautogui.moveTo(1030, 630)
    # pyautogui.click()
    # print("执行完===点击游客登录确定")
    # time.sleep(2)
    #
    # # 剪辑ico
    # pyautogui.moveTo(410, 1060)
    # pyautogui.click()
    # print("执行完===点击ico 弹出窗体")
    # time.sleep(2)
    #
    # # # 点击确定检测dll
    # pyautogui.moveTo(1030, 630)
    # pyautogui.click()
    # print("执行完===点击确定检测dll")
    # time.sleep(2)
    # # 剪辑ico
    # pyautogui.moveTo(410, 1060)
    # pyautogui.click()
    # print("执行完===点击ico 弹出窗体")
    # time.sleep(2)
    # #
    # # 点击确定过期提醒
    # pyautogui.moveTo(1030, 600)
    # pyautogui.click()
    # time.sleep(10)
    # #
    # # # 点击关闭升级
    # pyautogui.moveTo(1154, 663)
    # pyautogui.click()
    # time.sleep(4)
    # #
    # #
    # # # 点击开启预警
    # pyautogui.moveTo(960, 600)
    # pyautogui.click()
    # time.sleep(4)
    # #
    # # # 点击关闭广告
    # pyautogui.moveTo(1337, 253)
    # pyautogui.click()
    # time.sleep(2)
    #
    # # 程序最大化
    # pyautogui.hotkey('win', 'up')
    # # # 关闭程序
    # pyautogui.moveTo(1094, 13)
    # pyautogui.click()
    # time.sleep(2)
    # pyautogui.moveTo(853, 679)
    # pyautogui.click()
    # time.sleep(2)
    # # 点击选项
    # pyautogui.moveTo(1507, 7)
    # pyautogui.click()
    # time.sleep(0.5)
    # # 点击盘后数据升级
    # pyautogui.moveTo(1543, 252)
    # pyautogui.click()
    # time.sleep(0.5)
    #
    # # 点击数据开始升级
    # pyautogui.moveTo(1120, 700)
    # pyautogui.click()
    # time.sleep(0.5)
    #
    # # 点击自动选股
    # pyautogui.moveTo(97, 1006)
    # pyautogui.click()
    # time.sleep(1)
    #
    # # 点击一键选股
    # pyautogui.moveTo(114, 596)
    # pyautogui.click()
    # time.sleep(60)

    pass
if __name__ == '__main__':
    openTDX()

