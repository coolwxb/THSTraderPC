import time

import pyautogui
import pyperclip
import pywinauto



# 控制点击 txs软件
class Mss:
    def __init__(self, shared_lock):
        self.lock = shared_lock

    # 点击菜单栏上菜单 恢复前台显示
    def click_soft(self):
        pywinauto.keyboard.send_keys('{ESC}')
        pywinauto.keyboard.send_keys('{ESC}')
        # 判断软件是否在前台
        # 16,5
        # 获取当前光标位置
        fix = pyautogui.pixelMatchesColor(17, 16, (176, 6,6))
        if not fix:
            pyautogui.moveTo(230, 1068)
            pyautogui.click(230, 1068)
        time.sleep(1)

    # 点击同花顺交易系统 恢复前台显示
    def click_trade_soft(self):
        pywinauto.keyboard.send_keys('{ESC}')
        pywinauto.keyboard.send_keys('{ESC}')

        pyautogui.moveTo(271, 1061)
        pyautogui.click(271, 1061)
        time.sleep(1)

    # 进入紫色线预警模块
    def enter_zsxyj(self):
        pywinauto.keyboard.send_keys("jjzxyj")
        pywinauto.keyboard.send_keys("{ENTER}")
        time.sleep(1)

    # ctl+a 复制所有代码
    def copy_all_code(self):
        pyautogui.moveTo(988, 595)
        pyautogui.click(988, 595)
        pywinauto.keyboard.send_keys("^A")
        time.sleep(1)
        # 判断是否出现全选对话框
        fix = pyautogui.pixelMatchesColor(993, 425, (180, 47, 50))
        if fix:
            # pywinauto.keyboard.send_keys("Y")
            # 选择批量操作方式，点击是
            pyautogui.moveTo(1002, 598)
            pyautogui.click(1002, 598)
            time.sleep(1)

        # 点击全选中
        pyautogui.moveTo(1067, 590)
        pyautogui.click(1067, 590)
        time.sleep(0.5)

        # 点击批量标记
        pyautogui.moveTo(1066, 389)
        pyautogui.click(1066, 389)
        time.sleep(1)
        # 点击复制到剪贴板
        pyautogui.moveTo(1069, 827)
        pyautogui.click(1069, 827)
        time.sleep(1)

        # 防止复制不到发生错误
        pywinauto.keyboard.send_keys('{ESC}')
        pywinauto.keyboard.send_keys('{ESC}')
        # 将粘贴板内容复制到预警文档里
        with open("预警.txt", 'w',encoding='utf-8') as f:
            f.write('')
            content = pyperclip.paste()
            f.write(content)


    def call_tdx_alert(self):
        self.click_soft()
        self.enter_zsxyj()
        self.copy_all_code()


if __name__ == '__main__':
   pass
