import pyautogui # 用于模拟鼠标和键盘操作
import pygetwindow as gw # 用于获取和操作窗口
import recognize as re

# 定义一个函数，用于激活特定标题的窗口
def activate_window(title):
    # 尝试获取标题匹配的窗口
    window = gw.getWindowsWithTitle(title)[0]
    if window:
        window.activate()

# 根据谜题数组模拟游戏手柄输入
def simulate_controller_input(puzzle_matrix):
    for row in puzzle_matrix:
        for cell in row:
            if cell == 1:
                pyautogui.press('space')  # Assuming 'space' is the key for 'A' on the controller
            pyautogui.press('right')  # Move right on the controller
        pyautogui.press('down')  # Move down at the end of the row

game_window_title = 'Your Game Window Title'  # Replace with your game window title
activate_window(game_window_title)
simulate_controller_input(re.puzzle_matrix)