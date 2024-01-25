import pygetwindow as gw  # 用于获取和操作窗口
import recognize as re
from pynput.keyboard import Controller, Key  # 模拟硬件输入
import time

# 打印当前所有打开的窗口标题
def print_open_windows():
    for window in gw.getAllTitles():
        print(window)


# 用于激活特定标题的窗口
def activate_window(title):
    try:
        # 获取所有标题匹配的窗口
        windows = gw.getWindowsWithTitle(title)
        if windows:
            # 激活第一个匹配的窗口
            windows[0].activate()
            return True
        else:
            print(f"No window with title '{title}' detected.")
            return False
    except Exception as e:
        print(f"Error when trying to activate the window: {e}")
        return False


keyboard = Controller()


# 模拟按键输入
def press_key(key):
    keyboard.press(key)
    time.sleep(0.05)
    keyboard.release(key)


# 根据谜题数组模拟游戏手柄输入
def simulate_controller_input(puzzle_matrix):
    press_key(Key.space)  # 用于聚焦窗口
    time.sleep(0.5)
    for row in puzzle_matrix:
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
if activate_window(game_window_title):
    simulate_controller_input(re.puzzle_matrix)
else:
    print("Failed to activate the game window.")