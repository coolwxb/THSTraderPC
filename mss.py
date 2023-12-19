import time

import pyautogui
import pyperclip
import pywinauto
from PIL import ImageGrab


# 点击菜单栏上菜单 恢复前台显示
def click_soft():
    # 判断软件是否在前台
    # 16,5
    # 获取当前光标位置
    fix = pyautogui.pixelMatchesColor(16, 5, (242, 0, 0))
    if not fix:
        pyautogui.click(456, 1060)
    time.sleep(1)


# 进入紫色线预警模块
def enter_zsxyj():
    pywinauto.keyboard.send_keys("zsxyj")
    pywinauto.keyboard.send_keys("{ENTER}")
    time.sleep(0.5)

# ctl+a 复制所有代码
def copy_all_code():
    pywinauto.keyboard.send_keys("^A")
    # 点击全选中
    pyautogui.moveTo(1062, 589)
    time.sleep(0.5)
    pyautogui.click(1062, 589)
    time.sleep(0.5)
    # 点击批量标记
    pyautogui.moveTo(1035, 396)
    pyautogui.click(1035,396)
    time.sleep(0.5)
    # 点击复制到剪贴板
    pyautogui.moveTo(1068, 825)
    pyautogui.click(1068,825)

    time.sleep(0.5)
    # 点击关闭
    pyautogui.moveTo(1065, 730)
    pyautogui.click(1065, 730)
    # 将粘贴板内容复制到预警文档里
    with open("预警.txt", 'w') as f:
        f.write('')
        content = pyperclip.paste()
        f.write(content)


def call_tdx_alert():
    click_soft()
    enter_zsxyj()
    copy_all_code()


if __name__ == '__main__':
    click_soft()
    # enter_zsxyj()
    # copy_all_code()


#
# # Press PAGE UP then PAGE DOWN to type "foobar".
# keyboard.add_hotkey('page up, page down', lambda: keyboard.write('foobar'))


