import pygetwindow as gw  # 用于获取和操作窗口
from pynput.keyboard import Controller, Key  # 模拟硬件输入
import time
import numpy as np

default_delay = 0.03
action_delay = 1
change_page_delay = 5


# 打印当前所有打开的窗口标题
def print_open_windows():
    for window in gw.getAllTitles():
        print(window)


# 用于激活特定标题的窗口
def activate_window(_title):
    try:
        # 获取所有标题匹配的窗口
        windows = gw.getWindowsWithTitle(_title)
        if windows:
            # 激活第一个匹配的窗口
            windows[0].activate()
            return True
        else:
            print(f"No window with title '{_title}' detected.")
            return False
    except Exception as e:
        print(f"Error when trying to activate the window: {e}")
        return False


keyboard = Controller()


def load_puzzle_matrix_from_file(_file_path):
    # 读取文件并转换为整数类型的二维数组
    return np.loadtxt(_file_path, dtype=int).tolist()


# 切换关卡时的按键输入
def change_level(_level, _chapter):
    # 如果是特别关卡，有特别的切换方式
    if _chapter != 'Special':
        for _ in range(3):
            # 按Z键确定返回菜单和确认新画作
            press_key('z', change_page_delay)
            # 根据关卡数切换关卡
        if _level % 15 == 0:
            press_key('g', action_delay)
        elif _level % 5 == 0:
            press_key(Key.down, action_delay)
            for _ in range(4):
                press_key(Key.left, action_delay)
        else:
            press_key(Key.right, action_delay)
    else:
        # 按Z键确定返回菜单
        press_key('z', change_page_delay)
        if _level % 25 == 0:
            print("It's time to change page.")
            press_key('z', change_page_delay)
            press_key('g', change_page_delay)
        elif _level % 5 == 0:
            press_key(Key.down, action_delay)
            for _ in range(4):
                press_key(Key.left, action_delay)
        else:
            press_key(Key.right, action_delay)

    # 按Z键确认关卡切换
    press_key('z', change_page_delay)


# 模拟按键输入
def press_key(_key, _delay=default_delay):
    keyboard.press(_key)
    time.sleep(default_delay)
    keyboard.release(_key)
    time.sleep(_delay)


# 进入游戏后解谜的输入
def simulate_controller_input(_puzzle_matrix):
    press_key('q')
    for row in _puzzle_matrix:
        for cell in row:
            if cell == 1:
                press_key('z')
            press_key(Key.right)
        press_key(Key.down)
    time.sleep(change_page_delay)


# 打印当前所有打开的窗口
# print_open_windows()

# 激活游戏窗口
game_window_title = 'HatsuneMikuLogicPaintS'
