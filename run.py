import recognize
import input
import os

# 章节
chapter = "Lv3"
# 总关卡数
total_level = 150
# 脚本开始关卡
starting_level = 1

# 识别图片时，需要裁剪的坐标
# 15*15: (360, 852, 1050, 1540)
# 20*20: (365, 857, 1050, 1540)
crop_coord = (365, 857, 1050, 1540)
# 扫描间隔大小
# 15*15: 46
# 20*20: 34
cell_interval = 34
# 识别图片时，图片文件夹路径
folder_path = f'pic\\{chapter}'
# 图片文件名前缀
image_prefix = f'{chapter} - '
# 图片总数量
image_count = total_level

# 循环结束后是否需要展示最终的图像
show_final_image = False

# 定义识别时目标颜色和容差
target_color = (152, 143, 145)  # 目标颜色RGB值
tolerance = 30  # 容差


# 检查txt文件是否存在，是否已经识别过图片
def txt_file_exists(_level):
    file_name = f"txt\\{chapter}\\{chapter} - {str(_level).zfill(3)}.txt"
    return os.path.isfile(file_name)


def main(recognize_only=False, input_only=False):
    # 调用recognize.py中的函数
    # 识别图片，输出答案
    if not input_only:
        # 如果最后一关的答案都有，可以说明前关卡答案也存在
        if not txt_file_exists(chapter):
            recognize.process_images_and_save_results(
                folder_path,
                image_prefix,
                image_count,
                cell_interval,
                target_color,
                tolerance,
                crop_coord,
                show_final_image
            )

    # 调用input.py中的函数
    # 在游戏中进行自动化通关
    if not recognize_only:
        if input.activate_window(input.game_window_title):
            for level in range(starting_level, total_level + 1):
                file_name = f"txt\\{chapter}\\{chapter} - {str(level).zfill(3)}.txt"
                if os.path.isfile(file_name):
                    puzzle_matrix = input.load_puzzle_matrix_from_file(file_name)
                    input.simulate_controller_input(puzzle_matrix)
                    if level < total_level:
                        input.change_level(level)
                else:
                    print(f"File {file_name} does not exist.")
        else:
            print("Failed to activate the game window.")


# 只有直接运行这个程序才会执行
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run recognize or input processes for the game.\n'
                                                 '运行游戏的识别图片并保存答案或自动化通关程序')
    parser.add_argument('--recognize-only', action='store_true', help='Run only the recognize process.\n'
                                                                      '只运行识别图片并保存答案程序')
    parser.add_argument('--input-only', action='store_true', help='Run only the input process.\n'
                                                                  '只运行自动化通关程序')
    args = parser.parse_args()

    main(args.recognize_only, args.input_only)
