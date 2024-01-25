import pygetwindow as gw  # 用于获取和操作窗口
from pynput.keyboard import Controller, Key  # 模拟硬件输入
import time
import numpy as np
import os


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
def change_level(_level):
    for _ in range(3):
        # 按Z键确定返回菜单
        press_key('z')
        time.sleep(5)

    # 然后根据关卡数切换关卡
    if _level % 15 == 0:
        press_key('g')
        time.sleep(2)
    elif _level % 5 == 0:
        press_key(Key.down)
        time.sleep(2)
        for _ in range(4):
            press_key(Key.left)
            time.sleep(2)
    else:
        press_key(Key.right)
        time.sleep(2)

    # 按Z键确认关卡切换
    press_key('z')
    time.sleep(5)


# 模拟按键输入
def press_key(key):
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)


# 进入游戏后解谜的输入
def simulate_controller_input(_puzzle_matrix):
    time.sleep(1)
    for row in _puzzle_matrix:
        for cell in row:
            if cell == 1:
                # time.sleep(0.1)
                press_key('z')  # 使用对应的键位
            time.sleep(0.05)
            press_key(Key.right)  # 使用 pynput 的 Key.right 来模拟右键
        # ztime.sleep(0.1)
        press_key(Key.down)  # 使用 pynput 的 Key.down 来模拟下键


# 打印当前所有打开的窗口
# print_open_windows()

# 尝试激活游戏窗口
game_window_title = 'HatsuneMikuLogicPaintS'

# 章节数
Chapter = "Lv2"
# Lv2有150关
totalLevel = 150
# 从第23关开始
starting_level = 28

if activate_window(game_window_title):
    for level in range(starting_level, totalLevel+1):
        # 构建文本文件名
        file_name = f"txt\\{Chapter}\\{Chapter} - {str(level).zfill(3)}.txt"
        if os.path.isfile(file_name):
            # 加载谜题矩阵
            puzzle_matrix = load_puzzle_matrix_from_file(file_name)
            # 游戏内的输入，因此开始前要先进入starting_level关卡的游戏页面
            simulate_controller_input(puzzle_matrix)
            # 如果不是最后一关，切换到下一关
            if level < totalLevel:
                change_level(level)
        else:
            print(f"File {file_name} does not exist.")
else:
    print("Failed to activate the game window.")