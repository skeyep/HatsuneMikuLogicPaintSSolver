import cv2  # 导入OpenCV库，用于图像处理
import numpy as np  # 导入NumPy库，用于处理大型多维数组和矩阵
from os.path import isfile, join  # 用于路径操作，例如拼接路径


# 通过计算目标颜色占比来判断
def calculate_color_frequency(image, target_color, tolerance):
    """
    计算图像中目标颜色的频率。

    :param image: 要分析的图像块。
    :param target_color: 目标颜色的RGB值。
    :param tolerance: 容差值。
    :return: 目标颜色占图像块的比例。
    """
    # 计算与目标颜色相符的像素点数量
    min_color = np.array([target_color[0] - tolerance, target_color[1] - tolerance, target_color[2] - tolerance])
    max_color = np.array([target_color[0] + tolerance, target_color[1] + tolerance, target_color[2] + tolerance])
    color_mask = cv2.inRange(image, min_color, max_color)
    color_count = np.count_nonzero(color_mask)

    # 计算图像块的总像素点数量
    total_count = image.shape[0] * image.shape[1]

    # 计算频率
    frequency = color_count / total_count

    return frequency


# 输出裁剪后的图像，以便调试准确度
def draw_intervals(image, interval, color=(0, 0, 255), thickness=1):
    """
    在图像上按指定间隔画线。

    :param image: 裁剪后的图像。
    :param interval: 间隔大小。
    :param color: 线的颜色，默认为红色。
    :param thickness: 线的厚度，默认为1。
    :return: 带有间隔线的图像。
    """
    # 画水平线
    for y in range(0, image.shape[0], interval):
        cv2.line(image, (0, y), (image.shape[1], y), color, thickness)
    # 画垂直线
    for x in range(0, image.shape[1], interval):
        cv2.line(image, (x, 0), (x, image.shape[0]), color, thickness)
    return image


def draw_circle_on_cell(image, cell_center, cell_size, value, color_map={0: (0, 0, 255), 1: (255, 0, 0)}):
    """
    在指定的单元格中心绘制一个圆点。

    :param image: 要在其上绘制的图像。
    :param cell_center: 单元格的中心坐标。
    :param cell_size: 单元格的大小(宽度和高度)。
    :param value: 单元格的值，根据该值选择颜色。
    :param color_map: 值到颜色的映射。
    """
    # 计算单元格中心的坐标
    center_x = int(cell_center[0] + cell_size / 2)
    center_y = int(cell_center[1] + cell_size / 2)
    # 从映射中获取颜色
    color = color_map.get(value, (0, 255, 0))  # 默认为绿色圆点
    # 绘制圆点
    cv2.circle(image, (center_x, center_y), 5, color, -1)


# 匹配图像模板
def match_template(image, template, threshold):
    # 使用OpenCV的matchTemplate功能进行模板匹配，这里选择了归一化的相关系数匹配方法
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    # 从匹配结果中找到最大值及其位置
    try:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # 识别阈值
        if max_val >= threshold:
            return True
        return False
    except Exception as e:
        print(f"An error occurred: {e}")


# 定义一个函数来构建谜题矩阵
def build_puzzle_matrix(path, interval, threshold):
    # 读取预先准备好的模板图片，这些图片是事先准备的，用来与游戏中的图标进行匹配
    filled_template = cv2.imread(join(path, 'filled_template.jpg'), cv2.IMREAD_COLOR)
    empty_template = cv2.imread(join(path, 'empty_template.jpg'), cv2.IMREAD_COLOR)
    x_template = cv2.imread(join(path, 'x_template.jpg'), cv2.IMREAD_COLOR)

    # 检查模板图片是否正确加载
    if filled_template is None or empty_template is None or x_template is None:
        raise ValueError("One or more template images did not load correctly. Please check the file paths.\n "
                         "一个或多个模板图像未正确加载。请检查文件路径。")

    # 读取包含谜题答案的图片
    answer_image_full = cv2.imread(join(path, 'ans/answer.jpg'), cv2.IMREAD_COLOR)
    # 检查模板图片是否正确加载谜题答案的图片
    if answer_image_full is None:
        raise ValueError("The answer image did not load correctly. Please check the file path.\n"
                         "谜题答案的图片未正确加载。请检查文件路径。")

    # 定义裁剪坐标
    crop_start = (360, 850)
    crop_end = (1050, 1540)
    # 裁剪图片，因为默认读的图片是1080p的
    answer_image = answer_image_full[crop_start[0]:crop_end[0], crop_start[1]:crop_end[1]]
    # 请保证裁剪后的图片能被间隔整除
    print("Cropped image size:", answer_image.shape)
    # 在裁剪后的图像上按间隔画线
    answer_image_with_intervals = draw_intervals(answer_image.copy(), interval)

    # 创建一个空列表用来存放谜题的二维数组
    matrix = []
    # 通过滑动窗口的方式遍历答案图片
    for y in range(0, answer_image.shape[0], interval):
        row = []
        for x in range(0, answer_image.shape[1], interval):
            crop_img = answer_image[y:y + interval, x:x + interval]
            if crop_img.size == 0:
                raise ValueError(
                    f"Cropped image at position ({x}, {y}) is empty. Check the interval and image dimensions.\n "
                    f"({x}, {y}) 处的裁剪图像为空。检查间隔和图像尺寸。")

            x_match = match_template(crop_img, x_template, threshold)
            filled_match = match_template(crop_img, filled_template, threshold)
            empty_match = match_template(crop_img, empty_template, threshold)

            cell_value = 0  # 默认设置为1
            if filled_match or empty_match:
                cell_value = 1
            elif x_match:
                cell_value = 0

            row.append(cell_value)
            # 绘制圆点
            draw_circle_on_cell(answer_image_with_intervals, (x, y), interval, cell_value)
            # 显示图像
            cv2.imshow('Cropped Image with Intervals', answer_image_with_intervals)
            cv2.waitKey(20)  # 暂停500毫秒

        if row:
            matrix.append(row)

    cv2.destroyAllWindows()
    # 循环结束后展示最终的图像
    cv2.imshow('Final Image with All Circles', answer_image_with_intervals)
    cv2.waitKey(0)  # 等待直到有键被按下
    cv2.destroyAllWindows()

    return matrix


# 指定存放模板图片和答案图片的文件夹路径
folder_path = 'pic'
# 设置扫描间隔大小
cell_interval = 46
# 设置阈值
match_threshold = 0.5
# 使用定义好的函数构建谜题矩阵
puzzle_matrix = build_puzzle_matrix(folder_path, cell_interval, match_threshold)
# 打印谜题矩阵，以便查看和调试
print(np.array(puzzle_matrix))
